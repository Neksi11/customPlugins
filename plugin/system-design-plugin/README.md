# System Design Mastery Plugin

A comprehensive Claude Code plugin for system design, featuring three distinct approaches and intelligent agents that maintain consistency across sessions.

## 🎯 Overview

This plugin provides three proven methodologies for designing scalable systems from scratch, along with technology selection guidance and specialized agents for each approach.

## 📁 Plugin Structure

```
system-design-plugin/
├── plugin.json                          # Plugin manifest
├── README.md                            # This file
├── skills/                              # Design approach skills
│   ├── approach-1-planned.md          # Requirements-driven architecture
│   ├── approach-2-evolutionary.md     # Bottleneck-driven evolution
│   ├── approach-3-comprehensive.md    # Complete curriculum
│   └── tech-stack.md                  # Technology selection guide
└── agents/                              # Specialized agents
    └── system-design-architects.md     # All three approach agents
```

## 🚀 Quick Start

### Use a Specific Approach

```
# Approach 1: Planned Architecture (Best for known requirements)
I'm designing a music streaming service for 500K users. Use approach-1-planned.

# Approach 2: Evolutionary Architecture (Best for uncertain scale)
I'm building a startup MVP. Use approach-2-evolutionary.

# Approach 3: Comprehensive Learning (Best for interview prep)
I'm preparing for system design interviews. Use approach-3-comprehensive.
```

### Get Technology Recommendations

```
# For any approach
What database should I use for a social media app with 1M users?
What's the best load balancing strategy for my use case?
```

### Work with an Agent

```
# Architect Agent (Approach 1)
I need to design an e-commerce system. Act as system-design-planned-architect.

# Evolutionary Agent (Approach 2)
I need to build a scalable API. Act as system-design-evolutionary-architect.

# Mentor Agent (Approach 3)
I'm learning system design. Act as system-design-comprehensive-mentor.
```

## 📚 The Three Approaches

### Approach 1: Planned Architecture
**`approach-1-planned`** - Requirements-driven, bottom-up planning

- **Best for:** Known requirements, enterprise systems, when you have time to plan
- **Method:** Requirements → Capacity Planning → Architecture → Flows → API → Data → Scale
- **Focus:** Do the math first, design everything before coding
- **Key insight:** "Planning is 70%, Tech Selection is 20%, Coding is 10%"

### Approach 2: Evolutionary Architecture
**`approach-2-evolutionary`** - Bottleneck-driven, progressive complexity

- **Best for:** Uncertain scale, startups, rapid iteration
- **Method:** Start simple → Identify bottlenecks → Add complexity when proven needed
- **Focus:** Measure first, scale second, evolve incrementally
- **Key insight:** "Start with the simplest thing that works, add complexity only when needed"

### Approach 3: Comprehensive Curriculum
**`approach-3-comprehensive`** - Complete educational curriculum

- **Best for:** Learning system design, interview preparation, career growth
- **Method:** 10 modules covering all concepts from foundations to security
- **Focus:** Understand every layer before moving to the next
- **Key insight:** "Master system design by understanding every layer of the stack"

## 🛠️ Tech Stack Guide

**`tech-stack`** - Technology selection guide (accessible to all approaches)

Covers:
- Frontend (Mobile, Web)
- Backend API
- Databases (SQL vs NoSQL)
- Object Storage
- Caching
- Load Balancing
- Message Queues
- Monitoring & DevOps

## 🤖 The Agents

### System Design Architect (Planned)
**Agent:** `system-design-planned-architect`

- **Color:** Blue
- **Specialty:** Requirements-driven architecture
- **Style:** Professional, structured, detail-oriented
- **Best for:** Designing specific systems with known scale

### System Design Architect (Evolutionary)
**Agent:** `system-design-evolutionary-architect`

- **Color:** Green
- **Specialty:** Bottleneck-driven evolution
- **Style:** Pragmatic, iterative, simplicity-oriented
- **Best for:** Building from scratch with uncertain scale

### System Design Mentor (Comprehensive)
**Agent:** `system-design-comprehensive-mentor`

- **Color:** Purple
- **Specialty:** Complete education across all concepts
- **Style:** Educational, patient, comprehensive
- **Best for:** Learning, interview prep, career growth

## 💡 Usage Examples

### Example 1: Design a Music Streaming Service

```
I'm designing a Spotify-like music streaming service for 500K users and 30M songs.
Use approach-1-planned.

[Agent will guide you through:]
1. Requirements clarification
2. Capacity planning (90 TB audio storage calculation)
3. Architecture design
4. Read/Write flows
5. API endpoints
6. Database schema
7. Scale strategy
```

### Example 2: Build a Startup MVP

```
I'm building a social media app MVP. I don't know the scale yet.
Use approach-2-evolutionary.

[Agent will guide you through:]
1. Start with single server
2. Identify first bottleneck
3. Scale only when needed
4. Add load balancer when horizontal scaling is needed
5. Eliminate single points of failure
6. Evolve to multi-region when needed
```

### Example 3: Prepare for Interviews

```
I have a system design interview next week. Help me prepare.
Use approach-3-comprehensive.

[Agent will guide you through:]
1. Assess your current knowledge
2. Teach foundations (single server, DNS, request flow)
3. Cover databases (SQL vs NoSQL decision tree)
4. Explain scaling (vertical vs horizontal)
5. Practice load balancing algorithms
6. Design APIs (REST vs GraphQL vs gRPC)
7. Cover protocols (HTTP, WebSockets, TCP/UDP)
8. Explain authentication (OAuth2, JWT)
9. Explain authorization (RBAC, ABAC, ACL)
10. Cover security (rate limiting, CORS, CSRF, XSS)
```

## 🔑 Key Features

### Session Consistency
All agents maintain context across sessions:
- Remember architectural decisions made
- Keep track of requirements established
- Reference previous calculations and trade-offs
- Maintain evolution history (evolutionary approach)
- Track learning progress (comprehensive approach)

### Cross-Approach Integration
All approaches have access to:
- `tech-stack` skill for technology decisions
- Can reference other approaches when helpful
- Provide comparisons and recommendations

### Visual Learning
All skills include:
- ASCII diagrams for every concept
- Decision trees for complex choices
- Comparison tables for alternatives
- Code examples and configurations
- Best practices and common pitfalls

## 📖 Quick Reference Cards

### Approach 1 Quick Reference
```
1. What problem are we solving?        (Requirements)
2. How big is it?                     (Capacity)
3. What are the pieces?                (Architecture)
4. How does data flow?                (Flows)
5. How do we interact?                (API)
6. Where does data live?              (Data)
7. What breaks first?                 (Scale)
```

### Approach 2 Quick Reference
```
1. Start with single server model
2. Monitor and identify bottlenecks
3. Separate concerns (web tier ↔ data tier)
4. Choose database by asking questions
5. Scale vertical first, then horizontal
6. Add load balancer when needed
7. Eliminate single points of failure
8. Design APIs as contracts
9. Choose protocols based on patterns
10. Add authentication + authorization
11. Security by design
```

### Approach 3 Quick Reference
```
Modules 1-10: Foundations → Databases → Scaling → Load Balancing
→ Reliability → API Design → Protocols → Authentication
→ Authorization → Security
```

## 🎓 When to Use Each Approach

| Situation | Recommended Approach | Why? |
|-----------|---------------------|-------|
| Designing specific system with known requirements | Approach 1 (Planned) | Do the math upfront |
| Building MVP with uncertain scale | Approach 2 (Evolutionary) | Start simple, evolve |
| Learning for interviews/career growth | Approach 3 (Comprehensive) | Learn everything |
| Enterprise architecture with clear constraints | Approach 1 (Planned) | Plan thoroughly |
| Startup needing rapid iteration | Approach 2 (Evolutionary) | Move fast, adapt |
| Complete system design education | Approach 3 (Comprehensive) | Full curriculum |

## 🛠️ Installation

1. Copy the `system-design-plugin` folder to your Claude plugins directory:
   ```
   Windows: C:\Users\<username>\.claude\plugins\system-design-plugin
   Mac/Linux: ~/.claude/plugins/system-design-plugin
   ```

2. Restart Claude Code

3. The plugin will be automatically loaded

## 📝 Plugin Manifest

```json
{
  "name": "system-design",
  "version": "1.0.0",
  "description": "System Design Mastery - Three approaches for designing scalable systems",
  "keywords": [
    "system design",
    "architecture",
    "scalability",
    "api design",
    "database",
    "load balancing",
    "microservices",
    "distributed systems"
  ]
}
```

## 🤝 Contributing

This plugin is based on the System Design Mastery course materials. To extend:

1. Add new skills to the `skills/` directory
2. Add new agents to the `agents/` directory
3. Update `plugin.json` with new capabilities
4. Follow the skill and agent frontmatter format

## 📄 License

MIT License - Feel free to use and modify for your learning journey.

## 🎯 Credits

Based on the System Design Mastery approach, teaching developers how to design scalable systems from scratch and get to senior roles.

---

**Start designing like a senior engineer today!** 🚀
