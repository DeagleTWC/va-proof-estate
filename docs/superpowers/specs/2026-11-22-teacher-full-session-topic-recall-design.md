# Teacher V31 — Full Session Topic Recall

## Intent

Terry approved removing the arbitrary three-topic history limit so a visitor can revisit every distinct public lesson explored during the current visit. Public knowledge remains source-bound and the Teacher remains separate from Frankie.

## Scope and constraints

- Preserve the existing `createOpenConversationKernel({resolve,topics})` interface, `history()`, `ask('What have we covered?')`, and `choose(topicId)` behavior.
- Retain one most-recent snapshot per public, cited lesson topic, newest first, **without a numeric topic cap**. The public lesson catalog bounds distinct topic IDs in practice.
- Reopening a topic restores its original public question, explanation and source links; it may subsequently be followed by a short, contextual question.
- The history menu exposes only offered public topics. It cannot resolve an unoffered ID or protected content.
- Protected inquiries and explicit `reset()` clear the entire history. History is in-memory for the page session only; no browser storage, server service, private documents or Frankie integration.
- Keep the existing UI button and menu; update tests, public documentation, and asset cache version.

## Approaches

- **12 or 30 snapshots:** a larger but still arbitrary cap; simpler than full recall but needlessly drops earlier topics.
- **All distinct public topics in this page visit (selected):** reuse the existing ordered, de-duplicated in-page list; no additional service or cost.
- **Persistent long-term memory:** would require storage, retention policy and consent; outside this request.

## Verification

The fourth and fifth public lesson remain selectable. Revisit the oldest to verify its original source links and follow-up behavior. Repeat topics to verify uniqueness and newest-first order. Protected access and reset erase the list. The public release audit stays green.
