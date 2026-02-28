# ADR-0005: REST Boundary in v0; gRPC Documented for Future

## Status
Accepted

## Context
Meridian may evolve toward service separation where typed contracts and inter-service communication become relevant.

## Decision
Meridian v0 uses REST (FastAPI) as the serving boundary. Potential gRPC adoption is documented for future versions when logical boundaries become network boundaries.

## Alternatives Considered
- Implement gRPC in v0
- Keep transport unspecified

## Consequences
Positive:
- Reduces v0 complexity
- Preserves a clear evolution path

Negative:
- Future refactor required if services split