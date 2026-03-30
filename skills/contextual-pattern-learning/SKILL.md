---
name: contextual-pattern-learning
description: "Fingerprints projects by technology stack, architecture, and domain, then matches incoming tasks against stored patterns using weighted similarity scoring. Use when starting work in an unfamiliar codebase, adapting a solution from one language or framework to another, or estimating task complexity from historical data."
---

# Contextual Pattern Learning

Extracts multi-dimensional project context (technology stack, architecture, domain, team conventions) and uses weighted similarity scoring to find transferable patterns across codebases. Builds on the basic `pattern-learning` skill with richer context awareness.

## When to Apply

- Starting a new task in an unfamiliar codebase
- Adapting patterns from one technology/framework to another
- Estimating task complexity based on historical patterns
- Looking for similar solutions across projects

## Workflow

1. **Fingerprint the project** — detect languages, frameworks, architecture (MVC/microservices/etc.), and domain
2. **Calculate similarity** against stored patterns using weighted scoring:
   - Technology overlap: 40%
   - Problem type alignment: 30%
   - Scale and complexity: 20%
   - Domain relevance: 10%
3. **Assess transferability** — determine if the match is a direct transfer, needs technology adaptation, or requires full reimplementation
4. **Apply pattern** with appropriate adaptation strategy
5. **Record outcome** — capture context, execution details, and quality score to improve future matches

## Context Extraction

Inspect the project to build a fingerprint covering:

- **Technology stack**: Check `package.json`, `requirements.txt`, `Cargo.toml`, build configs for languages, frameworks, and libraries
- **Architecture**: Examine directory structure and imports to classify as monolith, microservices, serverless, etc.
- **Domain**: Identify business domain from naming conventions, README, and module organization
- **Team conventions**: Review git history for commit patterns, branching strategy, and coding style

## Similarity Scoring

```
Contextual Similarity =
  technology_overlap * 0.4 +
  problem_type_match * 0.3 +
  scale_compatibility * 0.2 +
  domain_relevance * 0.1
```

**Thresholds**: >= 0.85 high confidence (direct transfer), 0.60-0.85 moderate (adapt), < 0.60 low (consider alternatives).

## Pattern Transfer Strategies

| Strategy | When to Use | Modification Level |
|----------|------------|-------------------|
| Direct transfer | Same tech stack and domain | None |
| Technology adaptation | Same logic, different language/framework | Syntax and idioms |
| Architectural adaptation | Same approach, different structure | Module organization |
| Conceptual transfer | Similar problem, different domain | Full reimplementation |

## Pattern Lifecycle

1. **Capture**: Record task context, execution approach, skills used, and outcome quality
2. **Validate**: Cross-check against similar existing patterns for consistency
3. **Evolve**: Update success rates and transferability scores after each reuse
4. **Relate**: Map sequential, alternative, and prerequisite relationships between patterns

## Failure Prevention

Before applying a pattern, check:
- Context similarity >= 0.6 (below this, risk of mismatch is high)
- Required skills are available
- Required tooling exists in the target project
- Complexity is compatible with target scale

## Quality Metrics

- Context similarity accuracy: > 85%
- Pattern transfer success rate: > 75%
- Outcome prediction accuracy: > 80%

Integrates with `code-analysis` for structure extraction and `quality-standards` for quality assessment.