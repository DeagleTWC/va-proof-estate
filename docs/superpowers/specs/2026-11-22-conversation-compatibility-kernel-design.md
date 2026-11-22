# Conversation Compatibility Kernel — Public Teacher

## Intent

Terry Snyder approved one upstream Conversation Compatibility Kernel (CCK) after a live public-visitor review found that clear questions sometimes become generic clarification cards, relevant real-world context is replaced by unrelated examples, and natural disagreement can lose the lesson. CCK checks the proposed public response against the visitor's actual question before presentation. It serves the existing eleven subjects, not an additional subject.

## Approaches

1. Add more synonyms to the current router: small, but would not check the final answer or whether an exercise uses the visitor's context.
2. **Selected: one bounded public compatibility gate** between human-intent routing and the visible lesson. It can preserve a source-constrained direct answer for recognized public question classes, reject an unrelated follow-on teaching exercise, and let unclear questions remain open. Simple, testable, and no new external service.
3. Add an external language model: wider linguistic coverage but would require a new disclosure, privacy, cost and safety design. Not authorized for this cycle.

## Scope and non-goals

- Inputs: the visitor's latest public question, the human-intent candidate response, current local conversation context, and public topic records. No user text leaves the browser.
- Outputs: the unchanged candidate when compatible; a source-bound public lesson addressing a recognized exact question; or the existing gentle clarification when meaning is unresolved.
- Fix the observed LinkedIn failures: a warehouse pallet/withdrawn-approval question gets a bounded warehouse answer without payment-case substitution; a skeptical visitor gets a public evidence-status explanation and source links; a gravity-as-wave-array question gets a direct statement about what the public evidence cannot independently establish; ordinary-language disagreement stays attached to the prior question.
- Original field terms and question remain visible through simplification and reassurance. The protection gate always precedes CCK, and the kernel itself never overrides a protected result.
- When a field-specific example would otherwise be followed by an unrelated generic teaching exercise, suppress that exercise while preserving topic sources and the independently accessible eleven-lesson exercise bank.
- Maintain the DECLARED / OBSERVED / INDEPENDENTLY REPRODUCED distinction and refuse unsupported physical or mathematical certainty. Do not modify protected kernels or the native V.A. construction.
- The kernel is deterministic and bounded. It does **not** claim general semantic reasoning, resolve arbitrary mathematics, independently verify unprovided pilot originals, or silently select a popular interpretation.

## Acceptance

- The three observed public question classes answer their actual subject, show public sources, and keep unknowns explicit; source-specific replies remain intact through `Explain simply` and `I'm confused`.
- Natural disagreement variants trigger patient reconsideration without overwriting protected requests or swallowing a replacement question.
- An unrelated bank example is not shown beneath the warehouse answer. Generic and manually chosen lessons still expose the existing finite exercises.
- All existing eleven subjects, local privacy, public file audit, accessibility of the result controls, and versioned release checks remain intact.
