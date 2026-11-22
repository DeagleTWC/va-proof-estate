# Cognitive Reasoning Kernel — bounded public design

## Purpose

The Teacher should quietly check whether its reading of a visitor's turn is justified, then respond patiently when the visitor says the preceding answer was wrong. The visitor retains control of their question. Nothing here claims general cognition, independent discovery, or an established reversal of scientific knowledge.

## Approach and boundaries

- **Selected:** a hybrid, deterministic review layer. Examine every turn for an access boundary, an overt correction, and whether a routed topic is only inferred. Use the existing Human Interaction Kernel to request clarification on inferred routing; do not select a popular subject in its place.
- **Correction-only alternative:** simpler, but misses weak inferred routing on ordinary turns.
- **Every-turn elaborate reasoning alternative:** pretends the present static public Teacher can assess novel claims, so it is not justified by its evidence or architecture.
- **On correction:** when a visitor clearly rejects the prior lesson without giving a replacement question, acknowledge the mistake, state that interpretations (including apparently reversed ones) require evidence, invite patience, and ask which part was misunderstood. Do not defend the old topic or automatically select another.
- **On a substantive new question:** let the existing routing and access checks handle it, even if the visitor begins with a disagreement.
- **Access and privacy:** protected inquiries always take priority; no networking, persistence, private source, or Frankie bridge is added.
- **Presentation:** use the existing clarification panel and preserve the original question for the visitor's reference.

## Observable acceptance

- Visitor says "That's wrong" or "You misunderstood me" following a lesson: gets a patient correction prompt, not another lesson.
- Correction after a previously selected field lens remembers the actual original visitor question.
- A correction without prior lesson does not manufacture a remembered answer.
- "What went wrong with the test?" remains a genuine question, not presumed criticism.
- An overt correction containing a new, explicit question is routed to that question.
- A protected request disguised as a correction still receives the access boundary.
- All public release and privacy audits remain green.
