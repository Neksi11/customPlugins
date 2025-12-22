---
name: brainstorm
description: Quick exploration of multiple solution approaches for any problem or idea
model: sonnet
---

# Brainstorm Solutions

You are performing a quick brainstorming session to explore multiple solution approaches. Focus on breadth and creativity.

## Process

### 1. Quick Decode
Rapidly extract:
- What problem are we solving?
- What's the core constraint? (time, budget, complexity)
- What's the domain?

### 2. Generate Approaches
Generate 3-5 diverse approaches. Think broadly:

**Technology Categories:**
- No-code/Low-code (n8n, Zapier, Make, Airtable)
- Scripting (Python, Bash, Node.js scripts)
- Backend API (Express, Fastify, FastAPI, etc.)
- Serverless (Lambda, Cloud Functions, Vercel)
- Full Application (React, Vue, mobile apps)
- SaaS Integration (existing tools that already solve this)

**For each approach:**
```
[Approach Name]
- What it is: [1-sentence description]
- Best for: [When to use this]
- Not for: [When to avoid this]
- Complexity: [Low/Medium/High]
- Time: [Rough estimate]
- Example: [Concrete use case]
```

### 3. Generate Output

```markdown
# Brainstorm: [Problem Topic]

## Quick Summary
[1-2 sentences of what we're solving]

## Solution Approaches

### 1. [Approach Name] [Complexity]
**What:** [Description]
**Best for:** [Use case]
**Not for:** [Anti-pattern]
**Time estimate:** [Time]
**Key tools:** [Tools/libraries]

**Example:** [Concrete scenario]

### 2. [Approach Name] [Complexity]
[Same structure]

### 3. [Approach Name] [Complexity]
[Same structure]

## Quick Comparison

| Approach | Best For | Avoid If | Time |
|----------|----------|----------|------|
| [Name] | [Use case] | [Condition] | [Time] |
| ... | ... | ... | ... |

## Recommended Starting Point
[If user needs to build something soon, where should they start?]

## Questions to Narrow Down
1. [Question 1]
2. [Question 2]
3. [Question 3]
```

## Important Notes

- Keep it light and fast. This is for exploration, not deep analysis.
- Use the `/analyze` command for comprehensive analysis.
- Cover diverse approaches - don't just suggest different programming languages.
- Include non-code solutions when applicable (SaaS products, existing tools).

## When to Use This

- User asks "how to build X"
- User has an idea but no clear direction
- User wants to explore options before committing
- Early-stage ideation
