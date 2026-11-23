# Teacher V30 Session-History Design

## Intent

Let a visitor return to a public lesson discussed earlier in the same visit without repeating their question. Preserve the original public sources and field-specific explanation when revisiting. This is a measurable improvement in conversation usability, not a claim of general intelligence.

## Scope and boundaries

- Keep at most three distinct public lesson topics in temporary memory; the latest visit to a topic replaces its prior position.
- A visitor can ask "What have we covered?" or select a "Review earlier topics" button to see only public topic titles, then choose a prior lesson.
- Return the original explanation, field bridge, exact inquiry and source links; subsequent "Why?" or "Explain simply" follows the restored lesson.
- No browser storage, remote calls, private source, Frankie integration, account access, model costs or hidden automatic learning.
- Protected-access review runs ahead of history retrieval and clears session history; reset clears all history.
- Unrecognized requests still get patient clarification. Unoffered topic IDs never unlock a cached lesson.

## Approaches

1. Chosen: bounded in-page session history over the existing public conversation kernel. No new service or hosting bill. Only cited lessons are available.
2. Deferred: privately hosted open-ended reasoning. It could reason beyond the catalog but requires a reviewed service, access design and operating costs.

## Acceptance

Two different lessons, then "What have we covered?" must offer both. A chosen prior lesson must restore its cited answer; a follow-up must stay with it. Fourth distinct topic evicts the oldest. A protected request or reset must make the previous topics unavailable. The new button must behave identically to the typed request.
