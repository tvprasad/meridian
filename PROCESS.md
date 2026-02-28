\# Meridian Process



Meridian follows a small-team operating model with formal governance (even in single-developer execution).



\## Branching Model

\- Trunk-based development using `main` as trunk

\- Short-lived feature branches

\- No direct commits to `main`



\## Pull Requests

All changes merge via PR with mandatory review checklist.

CI must pass before merge.



\## ADR Policy

All changes that modify architectural invariants require a new ADR.

Architectural invariants include: control flow, failure semantics, confidence policy, provider boundaries, telemetry contract, evaluation policy, and transport strategy.



\## Definition of Done

A change is “Done” when:

\- Evaluation passes

\- Control invariants preserved

\- Telemetry intact

\- ADR added/updated if architectural

\- PR checklist completed



\## Releases

Semantic versioning:

\- v0.x.y for architecture stabilization

\- v1.0.0 for first deployable platform milestone

