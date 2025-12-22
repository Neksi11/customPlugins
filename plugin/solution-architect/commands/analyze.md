---
name: analyze
description: Deep analysis of an idea or problem with full decoding, requirements extraction, and solution recommendations
model: sonnet
---

# Analyze Idea or Problem

You are performing a deep analysis of a user's idea or problem. Your goal is to decode vague inputs into structured requirements and provide comprehensive solution recommendations.

## Process

### 1. Decode the Input
Extract and document:
- **Core Intent**: What does the user actually want to accomplish?
- **Domain**: What domain is this in? (web, mobile, automation, data, etc.)
- **Actors**: Who are the users/participants?
- **Data Flows**: What data moves through the system?
- **Implicit Requirements**: What's implied but not stated?

### 2. Identify Constraints and Gaps
- **Constraints**: Budget, timeline, skill requirements, infrastructure limitations
- **Gaps**: Critical information that's missing
- **Assumptions**: What are we assuming that needs validation?

### 3. Ask Clarifying Questions
If critical information is missing, ask targeted questions before proceeding:
- "What's your timeline for this?"
- "What's your budget range?"
- "What's your technical expertise level?"
- "Who are the end users?"
- "What scale are you expecting?"

### 4. Generate Problem Decomposition
Break down the problem into smaller, solvable components:
```
Main Problem
├── Sub-problem 1
│   ├── Component A
│   └── Component B
├── Sub-problem 2
└── Sub-problem 3
```

### 5. Map Solution Approaches
Identify 3-5 viable solution approaches. For each, specify:
- Approach name (e.g., "n8n Workflow", "Express API", "Serverless Function")
- Complexity level (Low/Medium/High)
- Estimated development time
- Cost estimate
- Scalability characteristics
- When to use this approach

### 6. Generate Output
Present your analysis in this format:

```markdown
# Analysis: [Project Name]

## 1. Problem Decoding

### Core Intent
[What user wants to accomplish]

### Requirements Extracted
**Functional:**
- [List functional requirements]

**Non-Functional:**
- [Performance, security, reliability needs]

### Constraints Identified
- [Budget, timeline, skill, infrastructure]

### Gaps Discovered
- [Questions that need answers]

## 2. Problem Decomposition
[Visual tree of sub-problems]

## 3. Solution Approaches

| Approach | Complexity | Time | Cost | Scalability | When to Use |
|----------|-----------|------|------|-------------|-------------|
| [Approach 1] | Low/Med/High | [Time] | [Cost] | Low/Med/High | [Use case] |
| [Approach 2] | ... | ... | ... | ... | ... |

## 4. Recommended Approach
**[Approach Name]**

**Rationale:**
- [Why this approach fits best]
- [Trade-offs accepted]
- [Key benefits]

## 5. Implementation Roadmap
[Priority-ordered list with estimates]

## 6. Next Steps
[Immediate actions user can take]
```

## Important Notes

- Be thorough but practical. Don't over-engineer simple problems.
- Use the specialized agents (Architecture Expert, Automation Specialist, etc.) for domain-specific insights.
- Always provide actionable next steps.
- If the user's request is truly vague, ask questions BEFORE generating solutions.

## Output File (Optional)

If the user wants to save the analysis, write it to:
```
docs/solution-analysis/[timestamp]-[topic-slug].md
```
