# ADR-0002: Deterministic Retrieval Threshold Enforcement

## Status
Accepted

## Context
Without threshold enforcement, systems generate answers under weak retrieval conditions and hallucination risk increases.

## Decision
Meridian v0 enforces a static retrieval confidence threshold. If retrieval_max_score < threshold, Meridian refuses generation with HTTP 422 and returns diagnostics.

## Alternatives Considered
- Always answer with disclaimers
- Dynamic/composite confidence scoring in v0

## Consequences
Positive:
- Stronger grounding guarantees
- Explicit control behavior

Negative:
- Requires tuning threshold per corpus
- More refusals in sparse corpora