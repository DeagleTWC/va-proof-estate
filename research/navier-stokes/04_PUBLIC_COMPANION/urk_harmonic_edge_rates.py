#!/usr/bin/env python3
"""Source-grounded, PUBLIC-SAFE harmonic edge rate examiner.

Implements only the explicit phase-interaction SPECIALIZATION of NAV-URK
Continuation 77, NOT a protected URK/New-K operator. Numeric outputs are
candidate measurements, not native URK admission or a Navier-Stokes proof.

Usage:
    python urk_harmonic_edge_rates.py --demo --output edge_rates.json
    python urk_harmonic_edge_rates.py --input example.json --output rates.json
"""
import argparse
import json
import math
from pathlib import Path

TOL = 1e-11


def vec_to_json(v):
    return [[float(z.real), float(z.imag)] for z in v]


def parse_mode(raw):
    k = raw["k"]
    if not isinstance(k, list) or len(k) != 3 or any(not isinstance(x, int) or isinstance(x, bool) for x in k):
        raise ValueError("Each k must be a list of three integers")
    k = tuple(k)
    if k == (0, 0, 0):
        raise ValueError("The zero phase is excluded in Continuation 77")
    u = raw["u"]
    if not isinstance(u, list) or len(u) != 3:
        raise ValueError("Each u must contain three [real,imaginary] pairs")
    try:
        v = tuple(complex(float(a[0]), float(a[1])) for a in u)
    except Exception as e:
        raise ValueError("Malformed complex vector") from e
    if not all(math.isfinite(c.real) and math.isfinite(c.imag) for c in v):
        raise ValueError("All amplitudes must be finite")
    return k, v


def dot(a, b):
    return sum((x*y for x, y in zip(a,b)), 0j)


def ksq(k):
    return sum(x*x for x in k)


def vnorm(v):
    return math.sqrt(sum(abs(x)**2 for x in v))


def proj(k, v):
    q = dot(k, v) / ksq(k)
    return tuple(v[i] - k[i]*q for i in range(3))


def plus(a,b):
    return tuple(a[i]+b[i] for i in range(3))


def negative(k):
    return tuple(-x for x in k)


def demo_input():
    eta = 1/1024
    positive = {
        (1,0,0): (0j,-1j*eta/2,eta/2+0j),
        (0,2,0): (eta/2+0j,0j,-1j*eta/2),
        (0,0,3): (-1j*eta/2,eta/2+0j,0j),
    }
    modes = dict(positive)
    for k,vec in positive.items():
        modes[negative(k)] = tuple(z.conjugate() for z in vec)
    return {
        "description": "Continuation 77 exact three-axis initial seed, eta=1/1024",
        "viscosity": 1.0,
        "rho": math.log(2),
        "initial_state": True,
        "modes": [{"k":list(k), "u":vec_to_json(u)} for k,u in sorted(modes.items())],
    }


def compute(data):
    nu = float(data["viscosity"])
    rho = float(data.get("rho", 0.0))
    if not (math.isfinite(nu) and nu > 0 and math.isfinite(rho) and rho >= 0):
        raise ValueError("Require viscosity > 0 and rho >= 0")
    modes = {}
    for raw in data["modes"]:
        k, v = parse_mode(raw)
        if k in modes: raise ValueError(f"Duplicate phase {k}")
        modes[k] = v
    if not modes: raise ValueError("At least one phase needed")
    solenoidal_error = max(abs(dot(k,v)) for k,v in modes.items())
    conj_error = max((max(abs(v[i] - modes.get(negative(k), (0j,)*3)[i].conjugate())
                          for i in range(3)) for k,v in modes.items()), default=0.0)
    conjugate_pairs_present = all(negative(k) in modes for k in modes)
    if solenoidal_error > TOL or not conjugate_pairs_present or conj_error > TOL:
        raise ValueError(f"Source-state invariants fail: k·U={solenoidal_error}, conjugacy={conj_error}, pairs={conjugate_pairs_present}")
    interaction = {}
    unprojected_source = {}
    edges = []
    for l in sorted(modes):
        ul = modes[l]
        for m in sorted(modes):
            k = plus(l, m)
            if k == (0,0,0):
                # Source states imply this source is identically zero.
                continue
            um = modes[m]
            s = tuple(dot(ul,m)*x for x in um)
            f = tuple(-1j*x for x in proj(k,s))
            unprojected_source[k] = plus(unprojected_source.get(k,(0j,)*3),s)
            interaction[k] = plus(interaction.get(k,(0j,)*3),f)
            uk = modes.get(k,(0j,)*3)
            power = (dot(tuple(z.conjugate() for z in uk), f)).real
            edges.append({
                "from_phase":list(l), "with_phase":list(m), "to_phase":list(k),
                "candidate_complex_amplitude_rate":vec_to_json(f),
                "amplitude_rate_magnitude":vnorm(f),
                "signed_child_kinetic_energy_rate":power,
                "status":"GENERATED_CANDIDATE_NOT_PROMOTED"
            })
    summaries=[]
    all_k = sorted(set(modes) | set(interaction))
    for k in all_k:
        uk = modes.get(k,(0j,)*3)
        source = interaction.get(k,(0j,)*3)
        linear = tuple(-nu*ksq(k)*z for z in uk)
        total = plus(source,linear)
        nonlinear_power = dot(tuple(z.conjugate() for z in uk),source).real
        heat = nu*ksq(k)*sum(abs(z)**2 for z in uk)
        item = {
            "phase":list(k), "originally_occupied":k in modes,
            "nonlinear_amplitude_rate":vec_to_json(source),
            "pressure_carrier_from_77_2": [float((-dot(k,unprojected_source.get(k,(0j,)*3))/ksq(k)).real), float((-dot(k,unprojected_source.get(k,(0j,)*3))/ksq(k)).imag)],
            "nonlinear_amplitude_rate_magnitude":vnorm(source),
            "linear_damping_amplitude_rate":vec_to_json(linear),
            "total_instantaneous_amplitude_rate":vec_to_json(total),
            "signed_nonlinear_kinetic_energy_rate":nonlinear_power,
            "viscous_heat_conversion_rate":heat,
            "total_kinetic_energy_rate":nonlinear_power-heat,
        }
        if k not in modes and vnorm(source) > TOL:
            item["new_child_energy_second_derivative_at_initial_instant"] = vnorm(source)**2
        summaries.append(item)
    epsilon = sum(math.sqrt(ksq(k))*math.exp(rho*math.sqrt(ksq(k)))*vnorm(v)
                  for k,v in modes.items())
    total_nl = sum(x["signed_nonlinear_kinetic_energy_rate"] for x in summaries)
    total_heat = sum(x["viscous_heat_conversion_rate"] for x in summaries)
    # The finite snapshot includes all supplied occupied modes. It is not an
    # infinite-time solution or full dynamical simulation.
    certificate = {
        "only_if_input_is_exact_initial_field": bool(data.get("initial_state",False)),
        "epsilon": epsilon, "threshold_nu_over_8": nu/8,
        "continuation_77_smallness_test_pass": bool(data.get("initial_state",False)) and epsilon < nu/8,
        "conditional_future_heat_increment_ceiling_4_epsilon_squared": (4*epsilon**2 if data.get("initial_state",False) and epsilon < nu/8 else None),
        "scope": "Continuation 77 analytically weighted, mean-zero, divergence-free periodic initial data only; conditional on its theorem, not a new proof",
    }
    return {
        "title":"URK Harmonic Edge Numerical Rates — Continuation 77 specialization",
        "provenance":{
            "original_URK_source":"UNIVERSAL RESOLVING KERNEL GENERATOR v0.1 (Samantha Revita & Terry Snyder)",
            "quantitative_law":"NAV–URK Continuation 77, equations (77.1),(77.2),(77.5)–(77.7)",
            "not_claimed":"Native protected NEW-K law, universal URK generator, unrestricted 3D regularity proof, or certified real-world consequence"
        },
        "definitions": {
            "edge":"ordered (ell,m) -> k=ell+m",
            "amplitude_rate":"-i * P_k[(U_ell dot m) U_m]",
            "signed_child_energy_rate":"Re(conjugate(U_k) dot edge_amplitude_rate), zero if U_k=0",
            "heat_rate":"nu |k|^2 |U_k|^2 per mode (normalized periodic-volume average)",
            "time":"instantaneous snapshot; all rates per unit of the model time"
        },
        "input_description":data.get("description", "user-supplied snapshot"),
        "input_mode_count":len(modes),"generated_ordered_edge_count":len(edges),
        "numerical_consistency":{
            "divergence_error": solenoidal_error,"conjugacy_error":conj_error,
            "nonlinear_energy_transfer_sum":total_nl,
            "nonlinear_energy_transfer_balance_pass":abs(total_nl)<TOL,
            "total_kinetic_decay_rate":total_nl-total_heat,
            "total_viscous_heat_conversion_rate":total_heat,
            "kinetic_heat_balance_residual":(total_nl-total_heat)+total_heat,
            "note":"Finite current-state algebraic consistency only; no time propagation performed."
        },
        "candidate_classification":"DREAM_OR_PAUSE_PENDING_ORIGINAL_URK_INVARIANT_CHECKS",
        "small_data_reference":certificate,
        "edges":edges,"phases":summaries
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    z=ap.add_mutually_exclusive_group(required=True)
    z.add_argument("--demo",action="store_true",help="Use exact Continuation 77 three-axis initial seed")
    z.add_argument("--input",type=Path,help="JSON state containing viscosity, rho, modes")
    ap.add_argument("--output",type=Path,default=Path("edge_rates.json"))
    ap.add_argument("--example-input",type=Path,help="With --demo, also write reusable input JSON")
    args=ap.parse_args()
    data=demo_input() if args.demo else json.loads(args.input.read_text(encoding="utf8"))
    if args.example_input:
        args.example_input.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    result=compute(data)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    target=next(x for x in result["phases"] if x["phase"]==[1,2,0]) if args.demo else None
    if target:
        print("Continuation 77 example child k=(1,2,0):",target["nonlinear_amplitude_rate"])
        expected=(-3/10485760,3/20971520,1j/4194304)
        got=[complex(*v) for v in target["nonlinear_amplitude_rate"]]
        assert max(abs(got[i]-expected[i]) for i in range(3)) < 1e-15, "Source F_k not reproduced"
        pressure=complex(*target["pressure_carrier_from_77_2"])
        assert abs(pressure-1j/5242880)<1e-15, "Source pressure p_k not reproduced"
        print("PASS: exact source child amplitude and pressure carriers reproduced")
    print("Edges:",result["generated_ordered_edge_count"])
    print("Epsilon:",result["small_data_reference"]["epsilon"])
    print("Heating rate:",result["numerical_consistency"]["total_viscous_heat_conversion_rate"])
    print("Nonlinear energy balance residual:",result["numerical_consistency"]["nonlinear_energy_transfer_sum"])
    print("Wrote",args.output)

if __name__ == "__main__":
    main()
