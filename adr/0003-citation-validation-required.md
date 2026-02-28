\# ADR-0003: Citation Validation as a Structural Requirement



\## Status

Accepted



\## Context

Responses without verifiable grounding reduce trust and make debugging difficult.



\## Decision

Meridian requires inline citations that map to retrieved chunks. Responses with missing or invalid citations fail validation and are returned as HTTP 422.



\## Alternatives Considered

\- Citations optional

\- Citations present but not validated



\## Consequences

Positive:

\- Improved trust and auditability

\- Reduced hallucination surface



Negative:

\- Increased prompt strictness and formatting requirements

