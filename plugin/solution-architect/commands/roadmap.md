---
name: roadmap
description: Generate step-by-step implementation roadmap with priorities and time estimates
model: sonnet
---

# Implementation Roadmap

You are generating a detailed implementation roadmap based on an analyzed problem and chosen approach.

## Process

### 1. Understand Context
- What problem are we solving?
- What approach has been chosen or recommended?
- What's the starting point? (from scratch, existing system, migration)
- What are the constraints? (timeline, budget, skills)

### 2. Decompose into Tasks
Break down the implementation into logical, ordered tasks:
- **Foundation**: What must be done first?
- **Core Features**: What delivers the main value?
- **Enhancement**: What makes it polished?
- **Polish**: What makes it production-ready?

### 3. Prioritize and Estimate
For each task:
- **Priority**: P0 (must have), P1 (should have), P2 (nice to have)
- **Dependencies**: What must be done first?
- **Time Estimate**: Realistic time for someone with appropriate skills
- **Skills Required**: What level/tech knowledge is needed?

### 4. Generate Output

```markdown
# Implementation Roadmap: [Project Name]

## Overview
**Approach:** [Chosen approach]
**Total Estimated Time:** [Range]
**Recommended Team Size:** [Solo/Pair/Team]

## Phase 1: Foundation (P0 - Must Have)
*Estimated: [Time]*

### 1.1 [Task Name]
**Priority:** P0 | **Time:** [Estimate] | **Dependencies:** None
**Skills Needed:** [Skill level]

**Description:**
[What this task accomplishes]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Definition of Done:**
- [ ] [Specific outcome]
- [ ] [Specific outcome]

**Resources:**
- [Links to docs/tools]

### 1.2 [Task Name]
[Same structure]

## Phase 2: Core Features (P0 - Must Have)
*Estimated: [Time]*

### 2.1 [Task Name]
[Same structure as above]

## Phase 3: Enhancement (P1 - Should Have)
*Estimated: [Time]*

[Tasks that add value but aren't critical]

## Phase 4: Production Readiness (P1 - Should Have)
*Estimated: [Time]*

[Security, monitoring, error handling, docs]

## Phase 5: Polish (P2 - Nice to Have)
*Estimated: [Time]*

[UI improvements, optimization, extra features]

## Critical Path
[Tasks that must be completed in order - the timeline is driven by these]

## Parallel Opportunities
[Tasks that can be done simultaneously by multiple people]

## Risk Areas
[Potential blockers or areas that might take longer]
- [Risk 1]: [Mitigation strategy]
- [Risk 2]: [Mitigation strategy]

## First Week Plan
**Week 1 Goals:**
- [ ] [Goal 1]
- [ ] [Goal 2]
- [ ] [Goal 3]

**Daily Breakdown:**
- **Day 1-2:** [Foundation tasks]
- **Day 3-4:** [Core tasks]
- **Day 5:** [Testing/iteration]

## Definition of Done
The project is complete when:
- [ ] [All P0 tasks done]
- [ ] [Core functionality working]
- [ ] [Basic testing passed]
- [ ] [Deployable to target environment]
```

## Important Notes

- Be realistic with time estimates. Everything takes longer than expected.
- Consider the user's skill level when estimating.
- Include learning time if the tech is new to them.
- Always include testing and documentation tasks.
- Focus on shipping value early. P2 tasks can wait.

## Time Estimation Guidelines

| Task Type | Solo (familiar) | Solo (learning) | Pair (familiar) |
|-----------|-----------------|-----------------|-----------------|
| Setup | 2-4 hours | 4-8 hours | 1-2 hours |
| Simple feature | 4-8 hours | 1-2 days | 2-4 hours |
| Complex feature | 1-3 days | 3-5 days | 1-2 days |
| Integration | 4-8 hours | 1-2 days | 2-4 hours |
| Testing | 20% of build | 30% of build | 20% of build |
| Docs | 2-4 hours | 4-8 hours | 1-2 hours |

## Common Phases by Approach

### n8n Workflow
1. Design workflow structure (2-4 hours)
2. Set up credentials and test connections (2-4 hours)
3. Build core workflow (4-8 hours)
4. Test and iterate (2-4 hours)
5. Document and hand off (1-2 hours)

### Backend API
1. Project setup and boilerplate (2-4 hours)
2. Database schema and migrations (2-4 hours)
3. Core endpoints (1-2 days)
4. Authentication/authorization (4-8 hours)
5. Validation and error handling (4-8 hours)
6. Testing (1-2 days)
7. Documentation (2-4 hours)

### Serverless Function
1. Project setup (1-2 hours)
2. Function logic (2-4 hours)
3. Environment configuration (1-2 hours)
4. Deployment setup (2-4 hours)
5. Testing and iteration (2-4 hours)
