# Comparative BYO examination and evidence custody

**Public-safe tools, no native V.A. execution or proprietary construction.** These tools operate on locally produced JSON reports. They do not run a submitted executable, contact an external server, validate real-world non-formation, or certify any engineering foundation.

## Same consequence, same declared test boundary

Two engineers can run the **same** synthetic generated matrix or persistent-session challenge with their own trusted adapters on their own machines. Freeze the protocol, seed, rounds, fixture digest, adapter version and local environment. Separately preserve each original report before comparison.

Matrix example (the second adapter is an intentionally unsafe negative control):

    python examiner/adversarial_matrix.py --seed 20261024 --rounds 2 --out /tmp/A.json --adapter python examiner/example_layer.py
    python examiner/adversarial_matrix.py --seed 20261024 --rounds 2 --out /tmp/B.json --adapter python examiner/negative_layer.py

The second run intentionally exits nonzero; its JSON report is still retained. Compare the reports:

    python examiner/compare_reports.py --left /tmp/A.json --right /tmp/B.json --left-id "Reference A" --right-id "Negative B" --out /tmp/comparison.json

The comparator **refuses** mismatched protocols, suite digests, seeds, rounds, case identities, report digests or internally contradictory outcomes. Its output preserves each side's observed responses and counts agreements/differences. It does not rank two complete architectures from the toy oracle.

The persistent-session route also supports the same comparison:

    python examiner/session_challenge.py --seed 20261024 --rounds 1 --out /tmp/session-A.json --adapter python examiner/session_reference.py
    python examiner/session_challenge.py --seed 20261024 --rounds 1 --out /tmp/session-B.json --adapter python examiner/session_broken.py
    python examiner/compare_reports.py --left /tmp/session-A.json --right /tmp/session-B.json --left-id "Reference A" --right-id "Negative B" --out /tmp/session-comparison.json

## Freeze a participant's report without uploading their code

    python examiner/evidence_custody.py seal --report /tmp/A.json --participant "Engineer A" --examiner "Examiner A" --artifact-id "adapter-A-revision-1" --artifact-file examiner/example_layer.py --out /tmp/A-custody.json
    python examiner/evidence_custody.py verify --envelope /tmp/A-custody.json --report /tmp/A.json --artifact-file examiner/example_layer.py

The artifact-file flag computes only a SHA-256 from local bytes; the source never leaves the participant's machine through this tool. Omitting artifact-file permits report custody without source disclosure, but the artifact's actual bytes are then **not bound**. Share only material cleared for public release. Keep the untouched reports and envelope, exact commands/environment, source commit, participant declaration, changed-condition observations, failures, negative controls and any separate independent witness artifacts.

## Evidence status and limitations

- **Verified here:** local JSON protocol/fixture consistency, reconstructed synthetic decision oracle, repeated-run bookkeeping, exact report bytes against a recorded SHA-256, and reported comparison differences.
- **Not verified here:** who generated any hash or record; an independent examiner's identity; private implementation; native V.A. runtime; real physical or external effect formation/non-formation; production safety; customer impacts; certification or legal entitlement.
- A self-contained digest can be recreated by any author. It is **integrity bookkeeping, not a signature or independent custody**. Actual independent witness reproduction requires separately identifiable examiner, frozen source, raw original evidence, chain of custody, retained negative controls, observed consequence and replay.
- **No promotion:** Nothing in these scripts edits the native V.A. claim register, changes public proof standing, or grants authority over protected construction.

For controlled/high-risk material use a separately approved secure transfer; **do not publish** customer data, secrets, executable uploads, proprietary mathematics, apparatus construction, or exploitation instructions in GitHub issues.
