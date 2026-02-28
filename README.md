# Meridian

**Architecture-first control plane for production-grade RAG and agentic AI systems.**

---

## Overview

Meridian is a governed, architecture-shaped reference implementation for retrieval-grounded AI systems.

It enforces:

- Deterministic retrieval thresholds  
- Explicit failure semantics  
- Citation validation  
- Offline evaluation discipline  
- Versioned architectural decisions (ADRs)  
- Structured telemetry logging  

Meridian separates probabilistic reasoning from deterministic control.

Control precedes generation.  
Observability precedes scale.  
Governance precedes automation.

---

## v0 Scope

Meridian v0 implements:

- Single-agent RAG with control discipline  
- Fixed-window chunking  
- Local embeddings + Chroma vector store  
- Local LLM via provider abstraction  
- Confidence scoring  
- Refusal semantics (HTTP 422)  
- JSON telemetry logging  
- Offline evaluation harness  

Non-goals for v0:

- Multi-agent orchestration  
- Tool execution boundaries  
- Multi-tenancy  
- gRPC transport  
- Cloud provisioning  

---

## Architecture

See:

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [PROCESS.md](PROCESS.md)
- [adr/](adr/)

---

## License

Apache 2.0