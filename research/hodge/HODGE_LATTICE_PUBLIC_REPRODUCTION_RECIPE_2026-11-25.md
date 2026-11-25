# Hodge / New K Exact Lattice Child v1 — Public Reproduction Recipe

**Research author:** Terry Allen Snyder · DeagleTWC / V.A. Proof Estate  
**Audit date:** 25 November 2026  
**Scope:** the declared Fermat quintic fourfold only; original author claims and earlier releases are preserved.

## Frozen input

- [Download the public-safe lattice child ZIP](https://drive.google.com/file/d/1m69eLgms780kuyok4y1eyAsTyh9MDxPJ/view?usp=drivesdk).
- ZIP name: `NEWK_HODGE_LATTICE_CLOSURE_CHILD_V1_2026-11-25.zip`.
- Expected ZIP SHA-256: `ee0d52bbe2cb5498c2aafc1e578e266dec5f4d72d614f05f2fe753bf320cb1e4`.
- Check the downloaded ZIP bytes with `sha256sum NEWK_HODGE_LATTICE_CLOSURE_CHILD_V1_2026-11-25.zip` (or your platform's equivalent) **before** extraction.
- Extract the archive, then enter the `HISTORY_KERNEL_V1` directory. The following commands use Python 3 and only the frozen files in that directory.

## Test the full child

```bash
python -m unittest discover -p 'test_*.py'
```

**Expected:** `Ran 39 tests` and `OK` (exit code 0). The tests include exact plane identification, Galois partition, Gram reconstruction, changed conditions, anchor refusal, altered evidence, and receipt replay.

## Run and replay the unchanged-condition gate

```bash
python lattice_closure_cli.py run --trusted-source-sha 7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23 --trusted-ledger-sha 569b52d99fc7ad1a5b96effacdb864422b82d00fe3fece353a7e171553f3c22b --output-prefix lattice_audit
python lattice_closure_cli.py replay --trusted-source-sha 7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23 --trusted-ledger-sha 569b52d99fc7ad1a5b96effacdb864422b82d00fe3fece353a7e171553f3c22b --output-prefix lattice_audit
```

**Expected:** `LATTICE_GATE CARRY`, `ORBIT_COUNT 480`, `GRAM_MOD_1009 437` (run exit 0), followed by `LATTICE_REPLAY_OK` (replay exit 0). The CLI creates `lattice_audit_receipt.json` and `lattice_audit_exact_evidence.json` for inspection.

## Challenge the gate: changed condition

The included `newk_lattice_changed_conditions.json` changes the declared degree from 5 to 6. It does not alter the frozen source.

```bash
python lattice_closure_cli.py run --trusted-source-sha 7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23 --trusted-ledger-sha 569b52d99fc7ad1a5b96effacdb864422b82d00fe3fece353a7e171553f3c22b --conditions-json newk_lattice_changed_conditions.json --output-prefix changed_audit
python lattice_closure_cli.py replay --trusted-source-sha 7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23 --trusted-ledger-sha 569b52d99fc7ad1a5b96effacdb864422b82d00fe3fece353a7e171553f3c22b --output-prefix changed_audit
```

**Expected:** `LATTICE_GATE REEXAMINE` (run exit 2) and `LATTICE_REPLAY_OK` (replay exit 0). Exit 2 is the intended changed-condition disposition, not a failed test.

## Challenge the gate: wrong trusted ledger

```bash
python lattice_closure_cli.py run --trusted-source-sha 7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23 --trusted-ledger-sha 0000000000000000000000000000000000000000000000000000000000000000 --output-prefix refused_audit
python lattice_closure_cli.py replay --trusted-source-sha 7966f67398ea83bbb8e4ec88e57f7307014148a0bbf8fdb37af7924f7e9d2d23 --trusted-ledger-sha 0000000000000000000000000000000000000000000000000000000000000000 --output-prefix refused_audit
```

**Expected:** `LATTICE_GATE REFUSE` (run exit 3), then `LATTICE_REPLAY_OK` (replay exit 0). Replay success means the *refusal* is reproducible; it does not turn a refused witness into an accepted witness.

## Frozen receipt identifiers

| Recorded case | SHA-256 |
|---|---|
| CARRY | `29518ef75bd3ca44178d817a10ec9e447bc051e08edd277753aa44371999f5c5` |
| REEXAMINE | `0933a81d247f33d12e67aaeec82509a9c435d50d76bad98a9b9e6b30c48d43dd` |
| REFUSE | `fe4bf1b48385f99c72c514ffa121dcb5ce7dc0db1a4d80224ff5098aec10782a` |
| Exact 401×401 Gram JSON | `091350e197c318cf910b57c2153ea2de45d9f7cc9517c2f548a7e3fee01ad834` |

These receipt hashes identify frozen package objects, not the newly generated local `*_audit_*` files. A local run's exact content is controlled by its input conditions and output prefix.

## What this establishes and what it does not

The finite-source witness reconstructs 1,875 plane descriptions, partitions them into 480 Galois orbits and obtains a 401-dimensional algebraic intersection witness with nonzero determinant modulo 1009. Its identification with the rational Hodge space uses a separately frozen 401-dimensional rational-character census for this specific (X_5).

**Not established by this audit:** a fresh proof of that census, unrestricted Hodge for every smooth projective variety, protected GEN 1056 authentication, or external referee acceptance. This added recipe changes no theorem claim and modifies no frozen parent evidence.

**Related records:** [formal statement](NEWK_LATTICE_CLOSURE_FORMAL_2026-11-25.md) · [machine manifest](NEWK_LATTICE_CLOSURE_MANIFEST.json) · [public Hodge page](../../hodge.html#hodge-newk-lattice-closure-child-v1).
