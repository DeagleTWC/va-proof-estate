# Human Interaction Kernel — Public Teacher design

**Intent:** Let the visitor's intended question govern the teaching path, rather than treating a keyword score as an answer. The Teacher should patiently seek understanding before routing uncertain language.

**Goals:** Clear questions continue to source-linked lessons. Unclear questions receive a gentle clarification and optionally relevant, nonbinding public paths. A follow-up can resolve the question without discarding the visitor's original example. A selected path is a visitor choice, not an automatic declaration of meaning.

**Non-goals:** Pretending to understand unconstrained language, fabricating a new answer, claiming native mathematical proof, adding an LLM or network service, or releasing protected construction.

**Constraints:** Offline browser-only processing. No storage, network call, or transmitted learner text. The existing `teach()` function remains the public-source and protected-access authority; an interaction step must not bypass it. Public terminology and eleven lesson exercises remain unchanged. UI uses text nodes and accessible buttons.

**Approaches considered:** (A) Add phrase-specific regex aliases — fast, but repeats the earlier downstream patch cycle. (B) Introduce a small stateful, deterministic interaction kernel over the current evidence router — preserves original questions and makes uncertainty visible. (C) Add a hosted conversational LLM — open-ended language coverage but new privacy, operational, and public-access dependencies. **Selected:** B, consistent with the user's direction to understand before teaching and the site's offline boundary.

**Behavior:** Explicit public subjects and protected review requests preserve their existing result. Ambiguous map results and routes inferred only from weak keyword scoring ask the visitor to clarify, with optional nonbinding candidate paths. A follow-up explicitly naming one of those paths retains the original field question. New unrelated questions begin a fresh local inquiry. Unsupported questions are not silently answered.
