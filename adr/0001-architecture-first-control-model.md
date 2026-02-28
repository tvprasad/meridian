# ADR-0001: Architecture-First Control Model

## Status
Accepted

## Context
RAG and agent systems often fail in production due to ambiguous execution behavior and missing governance boundaries.

## Decision
Meridian will implement a control-plane model that separates probabilistic reasoning (LLM) from deterministic governance (retrieval thresholds, failure semantics, citation validation, evaluation discipline).

## Alternatives Considered
- Model-centric design with best-effort answers
- Prompt-only governance without a control layer

## Consequences
Positive:
- Clear failure semantics and reduced ambiguity
- Reliable behavior under uncertainty

Negative:
- Higher refusal rate when context is insufficient
- Additional architectural complexity