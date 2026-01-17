# Update PROJECT_STATE.md Rule

PROJECT_STATE.md represents the current accepted architectural state of the project.

## Update Timing
- Do not update PROJECT_STATE.md during experimentation, debugging, or failed attempts
- Update PROJECT_STATE.md only after an implementation is explicitly accepted and will be carried forward

## What Counts as "Accepted"
An implementation is considered accepted when:
- It satisfies the phase's acceptance criteria or
- The developer explicitly confirms the approach will be kept (even if incomplete)

## What to Record
When updating PROJECT_STATE.md, summarize:
- New systems or components introduced
- Their responsibilities and boundaries
- Any architectural assumptions now relied upon
- Known gaps or deferred work

## What Not to Record
- Failed attempts
- Temporary hacks
- Debugging notes
- Internal implementation details

## Update Behavior
- Summaries must be concise and architectural, not implementation-level
- If unsure whether an implementation is accepted, ask for confirmation before updating