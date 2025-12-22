---
name: compare
description: Side-by-side comparison of different implementation approaches (n8n vs backend vs scripting vs serverless)
model: sonnet
---

# Compare Implementation Approaches

You are generating a detailed comparison matrix between different implementation approaches for a specific problem.

## Process

### 1. Identify the Problem
Understand what we're comparing approaches for:
- What problem are we solving?
- What are the key requirements?
- What are the constraints?

### 2. Select Approaches to Compare
Compare 3-5 approaches. Common categories:
- **n8n / Low-code workflow** (visual automation)
- **Backend API** (Express, Fastify, Django, etc.)
- **Serverless** (Lambda, Cloud Functions)
- **Scripting** (Python, Bash, Node.js)
- **Microservices** (distributed systems)
- **Monolithic app** (single deployed unit)
- **SaaS Integration** (use existing tools)

### 3. Comparison Criteria

For each approach, evaluate:

| Criterion | Description |
|-----------|-------------|
| **Complexity** | Technical difficulty (Low/Medium/High) |
| **Development Time** | Hours/weeks to build |
| **Cost** | Infrastructure + licenses + maintenance |
| **Scalability** | Max users/throughput before rearchitecture |
| **Flexibility** | Ease of making changes later |
| **Skills Required** | Technical level needed |
| **Maintenance** | Ongoing effort to keep running |
| **Time to First Value** | How fast to get something working |

### 4. Generate Output

```markdown
# Comparison: [Problem/Feature Name]

## Problem Statement
[What we're solving and key requirements]

## Comparison Matrix

| Aspect | n8n/Workflow | Backend API | Serverless | Scripting | SaaS |
|--------|-------------|-------------|------------|-----------|------|
| **Complexity** | Low | Medium | Medium | Low | Very Low |
| **Dev Time** | 1-3 days | 1-2 weeks | 3-5 days | 1 day | 0 days |
| **Monthly Cost** | $20-50 | $10-100 | $0-50 | $0-10 | $50-500 |
| **Max Scale** | ~10k runs | ~100k users | ~1M requests | ~1k runs | Unlimited |
| **Flexibility** | Medium | High | Medium | Low | Low |
| **Skills Needed** | Low | High | High | Medium | None |
| **Maintenance** | Low | Medium | Low | Low | None |

## Detailed Analysis

### 1. [Approach Name]

**Pros:**
- [Benefit 1]
- [Benefit 2]

**Cons:**
- [Drawback 1]
- [Drawback 2]

**Best for:**
- [Specific use cases]
- [When constraints match]

**Avoid if:**
- [Anti-patterns]
- [Requirements that don't fit]

**Example scenario:**
> [User story where this shines]

### 2. [Approach Name]
[Same structure]

## Recommendation Matrix

| If you want... | Use this approach |
|----------------|-------------------|
| Fastest to build | [Approach] |
| Lowest cost | [Approach] |
| Most control | [Approach] |
| Easiest to maintain | [Approach] |
| Best scalability | [Approach] |

## Suggested Approach
Based on typical scenarios: **[Recommended approach]**

**Why:**
[Your reasoning based on common use cases]

**Unless you...**
[Circumstances where you'd choose differently]
```

## Important Notes

- Be objective. Don't favor "cool" tech over practical solutions.
- Consider total cost of ownership, not just initial build.
- Factor in the user's likely skill level.
- Use data from `references/approaches.md` for consistent information.

## Quick Comparison Templates

### n8n vs Backend API
- **Choose n8n if**: Timeline < 1 week, budget < $500, mostly integrations, low custom logic
- **Choose Backend if**: Custom business logic, complex data processing, API needs to be consumed by others

### Scripting vs Serverless
- **Choose Scripting if**: One-time task, cron job, local execution is fine
- **Choose Serverless if**: API endpoint, unpredictable load, need pay-per-use
