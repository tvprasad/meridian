# ADR-0004: Offline Evaluation Harness as a Core Layer

## Status
Accepted

## Context
Production AI systems degrade without regression discipline and measurable baselines.

## Decision
Meridian includes an offline evaluation harness using a JSON baseline dataset. The evaluator runs all test cases, reports aggregate results, and is suitable for CI gating.

## Alternatives Considered
- Manual testing only
- API-exposed evaluation endpoint in v0

## Consequences
Positive:
- Regression detection and repeatability
- Enables disciplined iteration

Negative:
- Additional maintenance for baseline datasets