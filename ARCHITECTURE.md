\# Meridian Architecture



\## Preface: Architecture-First AI



Meridian is built on a single principle: production AI systems fail due to architectural ambiguity, not model weakness. Meridian implements a control-plane model that separates probabilistic reasoning from deterministic governance for retrieval-grounded AI systems.



Meridian v0 enforces:

\- Deterministic retrieval thresholds

\- Explicit failure semantics

\- Citation validation

\- Offline evaluation harness discipline

\- Provider abstraction boundaries

\- Versioned architectural decisions (ADRs)



Control precedes generation. Observability precedes scale. Governance precedes automation.



\## v0 Scope (Locked)



\### Goals

\- Single-agent RAG with control discipline

\- Multi-document corpus + metadata filtering

\- Fixed-window chunking

\- Local embeddings + Chroma vector store

\- Local LLM via provider abstraction

\- Strict citation enforcement

\- HTTP failure semantics + confidence\_score

\- Structured telemetry logging (JSON)

\- Offline evaluation harness (JSON dataset + script)



\### Non-Goals

\- Multi-agent orchestration

\- Tool execution boundary

\- Dynamic confidence scoring

\- DB-backed telemetry

\- Cloud provisioning

\- gRPC implementation (documented only)



\## Core Invariants

\- If retrieval confidence < threshold: refuse generation (HTTP 422)

\- Answers must contain verifiable citations to retrieved chunks

\- confidence\_score is retrieval-derived (v0: retrieval\_max\_score)

\- Every request produces trace\_id and telemetry event

