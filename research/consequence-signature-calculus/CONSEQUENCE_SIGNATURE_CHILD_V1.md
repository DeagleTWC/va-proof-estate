# Consequence Signature Calculus — exact public child v1

Author-origin source: Terry Snyder, *Universal Resolving Structure — Consequence Signature Calculus v1*, 30 April 2026, original six-page PDF, SHA-256 `e17250eca29c37e708b131795f43431510e4ae8e49dafcaaa6fc92f48a766e61`. The PDF is unchanged. This public child is an executable specialization of its declared model rules, not a new replacement manuscript.

## The source rule, its readings, and the single gate

The source gives the seven-component signature

\[\Sigma_C(x)=\langle\Phi(x),A(x),U(x),V(x),B(x),R(x),H(x)\rangle,\qquad\Phi(x)=C(x)-M(x)\]

and the stated binding criterion

\[\operatorname{Bind}(x)\iff\Phi(x)\ge0\land A(x)\ge0\land U(x)=1\land x\in\operatorname{Viab}(R)\land B(x)=0\land H(x)\ge H_{\min}.\]

The public child implements **one kernel, five invariant groups, one final gate**:

| Invariant group | Exact test on declared model inputs |
| --- | --- |
| Capacity and admissibility | `C - M >= 0` and `A >= 0` |
| Standing | `U == 1` |
| Viability | `state_id` is in the finite, *externally declared* viability set for `restart_id` |
| Breach | `B == 0` |
| Coherence | `H >= H_min` |

All numeric inputs are exact integers or rational strings, such as `"7/2"`, never binary floating-point coefficients. A failed invariant yields `REFUSE`.

Separately, the source's warning rule is

\[W=1\iff\dot\Phi<0\lor\dot A<0\lor\dot U<0\lor\dot V<0\lor\dot B>0\lor\dot H<0.\]

The child accepts six *declared* derivative readings. If the binding conjunction holds but the warning rule fires, its operational result is `PAUSE` for review; it separately records `bind_criterion_satisfied=true`. The source's `Bind` mathematical equivalence is not silently amended. If no invariant fails and no warning fires, the result is `BIND` **within the declared model only**.

## Reproduce and challenge

From the repository root:

```sh
python -m unittest discover -s research/consequence-signature-calculus -p 'test_consequence_signature_child_v1.py' -v
python research/consequence-signature-calculus/consequence_signature_child_v1.py --demo --receipt-dir /tmp/csc-public-receipts
python research/consequence-signature-calculus/consequence_signature_child_v1.py --verify /tmp/csc-public-receipts/bind-receipt.json
```

The CI workflow creates a fresh directory and uploads three JSON receipts: `BIND`, `REFUSE` (revoked standing), and `PAUSE` (falling reserve). Regeneration of the signed canonical input/output under the exact original PDF hash is required. Reordered dictionary keys or viability list order do not alter a receipt; forged standing, source, native-authentication fields, or digest fail verification. An existing receipt directory refuses overwrite.

## Source boundary and limits

- `Viab(R)` is a declared finite set, **not** an inferred complete viable corridor from a sealed URK/NEW K generator.
- Time derivatives are declared rational readings, **not** instrumented physical measurements.
- A SHA-256 receipt proves deterministic model replay and source-custody comparison, **not** empirical truth of supplied readings or universal consequence safety.
- `native_generator_authenticated` is always `false`. This public child does not reveal protected native materials and does not claim independent peer certification.

The intended next falsifier is an authenticated edge/viability source for a concrete state and restart, together with an independently inspectable mapping from measured readings to this model's seven signature components. Until then, the child tests the formal source's *conditional model logic*, exactly and transparently.
