#!/usr/bin/env python3
"""Independent public-equation reconstruction of saved 122/250-mode Fourier trajectories.

This is a newly written reference implementation of periodic 3D projected
Navier--Stokes Galerkin equations, NOT the unavailable original time-stepper
and NOT the protected URK/NEW-K mathematical operator. It uses NumPy and the
unmodified supplied six-mode Fourier seed. No external service or file writes
are needed except --output.

Expected run: python 05_REPRODUCIBILITY/independent_midpoint_replay.py
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import platform
import numpy as np

BASE = Path(__file__).resolve().parents[1]
NAMESPACE = "independent_reconstruction_from_public_fourier_law"


def seed_state():
    d=json.loads((BASE/"05_REPRODUCIBILITY/original_edge_rate_input_unmodified.json").read_text())
    return {tuple(r["k"]):np.array([complex(*z) for z in r["u"]],dtype=np.complex128) for r in d["modes"]}


def validate_seed(seed, tolerance=1e-14):
    if not seed: raise ValueError("Empty seed")
    for k,u in seed.items():
        if k==(0,0,0): raise ValueError("Zero mode")
        if tuple(-x for x in k) not in seed: raise ValueError("Missing conjugate")
        if np.max(np.abs(u-np.conjugate(seed[tuple(-x for x in k)])))>tolerance:
            raise ValueError("Conjugate symmetry violated")
        if abs(np.dot(k,u))>tolerance: raise ValueError("Transversality violated")
    return True


def make_system(R):
    lim=math.isqrt(R)
    modes=sorted((i,j,k) for i in range(-lim,lim+1)
                   for j in range(-lim,lim+1) for k in range(-lim,lim+1)
                   if 0<i*i+j*j+k*k<=R)
    vectors=np.asarray(modes,dtype=np.int64)
    mapping={p:i for i,p in enumerate(modes)}
    triads=[(j,mapping[q],mapping[tuple(x+y for x,y in zip(p,q))])
            for j,p in enumerate(modes) for q in modes
            if tuple(x+y for x,y in zip(p,q)) in mapping]
    l,m,k=np.asarray(triads,dtype=np.int64).T
    ksq=np.sum(vectors*vectors,axis=1).astype(float)
    return modes,vectors,mapping,l,m,k,ksq


def nonlinear(U, vectors,l,m,k,ksq):
    # N_k(U)=-i P_k sum_{ell+m=k} (U_ell . m) U_m.
    edge_dot=np.sum(U[l,:]*vectors[m,:],axis=1)
    source=np.zeros_like(U)
    np.add.at(source,k,edge_dot[:,None]*U[m,:])
    longitudinal=np.sum(source*vectors,axis=1)
    source-=vectors*(longitudinal/ksq)[:,None]
    return -1j*source


def integrate(radius2, steps=16, dt=0.0125, viscosity=1.0, max_iterations=40):
    modes,vectors,mapping,l,m,k,ksq=make_system(radius2)
    seed=seed_state();validate_seed(seed)
    if not set(seed).issubset(mapping):
        raise ValueError("Requested Galerkin cutoff omits a seed mode")
    U=np.zeros((len(modes),3),dtype=np.complex128)
    for mode,v in seed.items(): U[mapping[mode]]=v
    start=U.copy()
    kinetic_initial=float(0.5*np.sum(np.abs(U)**2))
    converted=0.0
    iterations=[]
    max_residual=0.0
    a=0.5*dt*viscosity*ksq[:,None]
    for _ in range(steps):
        # Solve exact implicit midpoint equations by fixed-point iteration,
        # rearranging the viscous diagonal to improve numerical stability.
        next_u=((1-a)/(1+a))*U
        for iteration in range(1,max_iterations+1):
            midpoint=0.5*(U+next_u)
            candidate=((1-a)*U+dt*nonlinear(midpoint,vectors,l,m,k,ksq))/(1+a)
            change=float(np.max(np.abs(candidate-next_u)))
            next_u=candidate
            if change<1e-16:break
        else: raise ArithmeticError("Midpoint solver failed to converge")
        midpoint=0.5*(U+next_u)
        residual=next_u-U-dt*(-viscosity*ksq[:,None]*midpoint + nonlinear(midpoint,vectors,l,m,k,ksq))
        max_residual=max(max_residual,float(np.max(np.abs(residual))))
        converted+=float(dt*viscosity*np.sum(ksq*np.sum(np.abs(midpoint)**2,axis=1)))
        U=next_u
        iterations.append(iteration)
    initial=kinetic_initial
    final=float(0.5*np.sum(np.abs(U)**2))
    max_divergence=float(np.max(np.abs(np.sum(U*vectors,axis=1))))
    max_reality=float(max(np.max(np.abs(U[i]-np.conj(U[mapping[tuple(-x for x in p)]]))) for i,p in enumerate(modes)))
    return {'initial_energy':initial,'final_energy':final,'total_heat_conversion':converted,
            'ledger_residual':initial-final-converted,'max_midpoint_equation_residual':max_residual,
            'mode_count':len(modes),'directed_triad_count':len(k),'step_count':steps,'dt':dt,
            'max_iterations':max(iterations),'divergence_residual':max_divergence,
            'reality_residual':max_reality,'final_modes':U,'mode_to_index':mapping,'initial_modes':start,
            'nonlinear_initial':nonlinear(start,vectors,l,m,k,ksq)}


def run():
    checks=[]; reports=[]
    def check(name,ok,detail):
        checks.append({'name':name,'passed':bool(ok),'detail':detail})
    seed=seed_state()
    check('seed-validity',validate_seed(seed),"six original public seed modes")
    bad={k:v.copy() for k,v in seed.items()};bad.pop((0,0,-3))
    try:validate_seed(bad);rejected=False
    except ValueError:rejected=True
    check('negative-control-missing-conjugate',rejected,"intentionally incomplete input rejected")
    bad={k:v.copy() for k,v in seed.items()};bad[(1,0,0)][0]+=1e-4
    try:validate_seed(bad);rejected=False
    except ValueError:rejected=True
    check('negative-control-violated-divergence',rejected,"intentionally non-solenoidal input rejected")

    for R,expected_modes,expected_triads in [(9,122,6642),(14,250,28938)]:
        current=integrate(R)
        saved=json.loads((BASE/f'04_EVIDENCE_AND_TECHNICAL_SUPPLEMENTS/GEN_{expected_modes}_Mode_16_Step_Recorded_Output.json').read_text())
        stored={tuple(r['k']):np.array([complex(*v) for v in r['u']],dtype=np.complex128) for r in saved['final_nonzero_modes']}
        max_field=float(max(np.max(np.abs(current['final_modes'][current['mode_to_index'][key]]-value)) for key,value in stored.items()))
        energy_difference=abs(current['final_energy']-saved['final_energy'])
        heat_difference=abs(current['total_heat_conversion']-saved['total_heat_conversion'])
        check(f'{expected_modes}-geometry',current['mode_count']==expected_modes and current['directed_triad_count']==expected_triads,f"{expected_modes} modes; {expected_triads} ordered triads")
        check(f'{expected_modes}-saved-endpoint',max_field<1e-12,f'max amplitude absolute error {max_field:.4e}')
        check(f'{expected_modes}-energy',energy_difference<1e-13,f'absolute final-energy difference {energy_difference:.4e}')
        check(f'{expected_modes}-heat',heat_difference<1e-13,f'absolute accumulated-heat difference {heat_difference:.4e}')
        check(f'{expected_modes}-independent-custody',abs(current['ledger_residual'])<1e-15,f"reconstructed K(0)-K(T)-H = {current['ledger_residual']:.4e}")
        check(f'{expected_modes}-numerical-invariants',current['divergence_residual']<1e-12 and current['reality_residual']<1e-12 and current['max_midpoint_equation_residual']<1e-12,
              f"divergence {current['divergence_residual']:.3e}; reality {current['reality_residual']:.3e}; midpoint eq {current['max_midpoint_equation_residual']:.3e}")
        half=integrate(R,steps=32,dt=0.00625)
        refined_diff=abs(half['final_energy']-current['final_energy'])
        check(f'{expected_modes}-timestep-refinement',refined_diff<1e-8,f'16-step vs 32-step final-energy difference {refined_diff:.4e}; not continuum convergence')
        reports.append({'cutoff_radius_squared':R,'modes':expected_modes,'triads':expected_triads,'steps':16,'dt':0.0125,
                        'saved_final_energy':saved['final_energy'],'independent_final_energy':current['final_energy'],
                        'absolute_final_energy_difference':energy_difference,
                        'saved_total_heat':saved['total_heat_conversion'],'independent_total_heat':current['total_heat_conversion'],
                        'absolute_heat_difference':heat_difference,
                        'max_saved_mode_amplitude_difference':max_field,
                        'independent_energy_ledger_residual':current['ledger_residual'],
                        'max_midpoint_equation_residual':current['max_midpoint_equation_residual'],
                        'max_reality_residual':current['reality_residual'],
                        'max_divergence_residual':current['divergence_residual'],
                        'max_fixed_point_iterations':current['max_iterations'],
                        'double_resolution_energy_difference':refined_diff})
    return {
        'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL',
        'scope':'Independent finite-mode Galerkin midpoint reconstruction from public Fourier equations; not the original trajectory integrator, protected URK/NEW-K source, or a continuum regularity proof',
        'model':'Unforced incompressible periodic three-dimensional Fourier Galerkin with viscosity 1; source seed reproduced without modification',
        'runtime':{'python':platform.python_version(),'numpy':np.__version__},
        'counts':{'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'total':len(checks)},
        'checks':checks,'runs':reports
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='write full JSON audit report')
    options=parser.parse_args()
    result=run()
    content=json.dumps(result,indent=2)+'\n'
    if options.output:
        options.output.write_text(content)
        print(f"Independent midpoint replay: {result['counts']['passed']}/{result['counts']['total']} checks PASS; report {options.output}")
    else:
        print(content)
    raise SystemExit(0 if result['status']=='PASS' else 1)
