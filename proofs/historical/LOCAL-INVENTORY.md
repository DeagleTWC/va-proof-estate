# Milestone 08 — Offline historical pilot and freeze discovery

**Working status:** The scanner and its synthetic regression tests are public; no private original, customer evidence, pilot result or historic frozen source has been uploaded by this milestone.

Many historical pilots, engineering layers and original freezes predate the October 2026 public Proof Estate. A **fingerprint inventory** of locally selected files is a practical discovery instrument, **not** a new historical freeze, proof of their original creation dates, confirmation of independent witnesses, or publication authorization.

## Offline use (Python 3.11+)

Clone or download the current public Proof Estate source. Use your own computer with *authorized access* to a chosen **private** folder of original source artifacts. Select only material you are allowed to inspect. No network service, GitHub token, site upload or application login is used by this script.

Store the private report **outside** the folder being scanned. Scan files recursively; common generated dependency folders (`.git`, `.venv`, `venv`, `node_modules`, `__pycache__`, `.pytest_cache`) are excluded and reported. Any symlink causes refusal, not traversal.

```bash
python scripts/historical_freeze_inventory.py scan \
  --root "/private/path/to/originals" \
  --out "/private/path/to/inventory.json"
```

The result contains each file's relative path, byte length and SHA-256, together with a checksum of the sorted inventory. It does **not** copy original file bytes or claim file-system modification dates are historical freeze dates. Paths and digests can themselves be sensitive; the resulting report is labeled **PRIVATE** and created without overwriting existing output, with restrictive local permissions. **Do not upload or publish it.**

After the original files are independently secured, recheck **current bytes** against the saved inventory:

```bash
python scripts/historical_freeze_inventory.py verify \
  --root "/private/path/to/originals" \
  --inventory "/private/path/to/inventory.json"
```

A mismatch detects changed, missing or added current files; it does not prove which revision was historically frozen.

Choose **one** exact relative file path to produce an *incomplete private candidate* with only the locally rechecked SHA-256 inserted:

```bash
python scripts/historical_freeze_inventory.py select \
  --root "/private/path/to/originals" \
  --inventory "/private/path/to/inventory.json" \
  --relative-path "selected/original-file.zip" \
  --out "/private/path/to/candidate.json"
```

**Important:** The candidate leaves original source ID, original freeze date, pilot/run identity, observations, custody, independent witness and release authorization unset. It therefore **fails** the public [historical carrier admission gate](ADMISSION-GUIDE.md) until originals are checked and cleared by their lawful custodians. This separation is deliberate.

## Windows PowerShell example

Run these as separate commands in a local PowerShell terminal, from the cloned proof-estate repository. Replace the example paths with folders you own or are authorized to inspect. Keep both outputs in a private location outside the original files and outside cloud-synced public folders.

```powershell
py -3 scripts/historical_freeze_inventory.py scan --root "C:\\PrivateProof\\Originals" --out "C:\\PrivateProof\\inventory-private.json"
py -3 scripts/historical_freeze_inventory.py verify --root "C:\\PrivateProof\\Originals" --inventory "C:\\PrivateProof\\inventory-private.json"
py -3 scripts/historical_freeze_inventory.py select --root "C:\\PrivateProof\\Originals" --inventory "C:\\PrivateProof\\inventory-private.json" --relative-path "frozen-build.zip" --out "C:\\PrivateProof\\candidate-private.json"
```

On Windows, the output-file creation flags do not themselves establish a private NTFS access-control list. Verify your folder permissions and disk encryption before scanning sensitive originals. No report is transferred to GitHub by these commands. **Do not upload either resulting JSON file.**

## What this milestone resolves

- Multiple distinct historical files can be inventoried without conflating them with six selected public proof surfaces or the new Cycle 001.
- Repeated revisions with identical hashes are still retained as separately named local paths. Neither a hash collision nor duplicate content confers independent proof.
- Original freeze identity remains under original custody; a later public extract receives its own separate authorization, publication date and digest.
- Failed scans produce no partial report; symlinks, changed bytes, overwrite requests and unsafe output placement fail closed.
- Publication is **never automatic**. Private inventory files and their generated candidates are not GitHub proof carriers.

## Hard stop before the public website

A public claim requires an inspectable source and authorized release scope. Review the exact [historical original/public-extract guide](ADMISSION-GUIDE.md), the [currently admitted public register](PUBLIC-CARRIER-REGISTER.json), and the [blank reviewer packet](../REVIEWER-PACKET-TEMPLATE.md). Each native V12 or KCD physical test has its own distinct proof requirements; nothing in an offline scan promotes it.

## Test locally

```bash
python scripts/test_historical_freeze_inventory.py
python scripts/validate_historical_carriers.py
```

These synthetic unit tests do not examine any original private pilot or protected substrate.
