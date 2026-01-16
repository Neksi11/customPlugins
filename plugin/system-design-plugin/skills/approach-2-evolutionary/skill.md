---
name: approach-2-evolutionary
description: Approach 2: Evolutionary Architecture (Progressive Complexity). Start with the simplest thing that works, add complexity ONLY when you can prove it's needed. Identify bottlenecks first, then scale. Best for uncertain scale and rapid iteration.
version: 1.0.0
---

# Approach 2: Evolutionary Architecture

## Overview
Start simple, identify bottlenecks, add complexity only when proven necessary. Every component exists to solve a specific problem, not because it's "standard architecture."

## The Evolutionary Mindset

**MID-LEVEL THINKING:**          **SENIOR THINKING:**
"I need Kubernetes"              "What's the problem?"
"I need microservices"            "What are the constraints?"
"I need NoSQL"                   "What data do I have?"
"I need event sourcing"          "What's the bottleneck?"

Mid-levels start with SOLUTION. Seniors start with PROBLEM.

## The 11 Phases of Evolution

### Phase 1: Single Server Mental Model
Every complex system starts simple:
```
USER → DNS → SINGLE SERVER (Web + API + DB + Cache)
```

**Questions to Ask:**
- Can this handle our expected load?
- What's the maximum users before we hit limits?
- What fails first? (CPU, RAM, Disk, Network)
- Is there a single point of failure? (YES - everything!)

### Phase 2: Identify Bottlenecks
**Measure BEFORE you act:**
- Monitor: CPU, Memory, Disk I/O, Network I/O, Response time, Request rate
- Symptom → Cause → Solution

**Common Bottlenecks:**
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| CPU at 100% | Heavy compute | More cores |
| Memory full | Memory leak | More RAM |
| Slow queries | DB bottleneck | Optimize DB |
| Network saturation | Too much traffic | More bandwidth |

### Phase 3: Separate Concerns
Split by responsibility:
```
WEB TIER (stateless) ↔ DATA TIER (stateful)
```

### Phase 4: Database Selection
**Ask questions, don't memorize:**

```
Q1: How STRUCTURED is your data?
    ├── Highly structured → SQL (PostgreSQL, MySQL)
    ├── Semi-structured → Document Store (MongoDB)
    └── Unstructured → NoSQL (Redis, Cassandra)

Q2: How important is CONSISTENCY?
    ├── Critical (payments) → SQL with ACID
    └── Eventually OK → NoSQL

Q3: What's your ACCESS PATTERN?
    ├── Complex joins → SQL
    ├── Key-value → Redis
    ├── Time-series → InfluxDB
    ├── Graph → Neo4j
    └── Full-text search → Elasticsearch

Q4: What's your SCALE trajectory?
    ├── Stays small → Anything works
    ├── Medium growth → SQL + read replicas
    └── Massive scale → Consider sharding/NoSQL
```

### Phase 5: Scaling Strategy
**Vertical (Scale Up):** Add more resources to one server
- Simple, no architecture change
- Hard limit, single point of failure
- Use for: Early stage, unknown scale

**Horizontal (Scale Out):** Add more servers
- No theoretical limit, fault tolerance
- More complex, needs load balancer
- Use for: Beyond single server limit, need fault tolerance

**Strategy:** Scale vertical until cost/benefit doesn't make sense, then go horizontal.

### Phase 6: Load Balancing
Algorithms:
1. **Round Robin** - Sequential rotation, similar servers
2. **Least Connections** - Route to least busy server
3. **Least Response Time** - Route to fastest + least busy
4. **IP Hash** - Same client always to same server (session affinity)
5. **Weighted** - Based on server capacity
6. **Geographic** - Route to nearest server
7. **Consistent Hashing** - Hash ring, consistent client routing

**Health Checks:**
- Continuously monitor server health
- Stop traffic to failed servers
- Resume when server recovers

### Phase 7: Eliminate Single Points of Failure
Common SPoFs: Load Balancer, Database, Cache, Auth Service

**Solutions:**
- **Redundancy:** Multiple instances (primary + standby)
- **Health Checks:** Monitor all components
- **Self-healing:** Auto-replace failed instances

### Phase 8: API Design
**Choose based on needs:**
- **REST**: Simple, standard HTTP, cache-friendly
- **GraphQL**: Flexible queries, single endpoint, complex UIs
- **gRPC**: High performance, binary, microservices communication

**API Design Principles:**
- **PREDICTABLE**: If /users/{id} exists, /users should exist
- **CONSISTENT**: Same response structure, error format everywhere
- **SIMPLE**: Intuitive resource names, minimal required fields
- **SECURE**: Authentication, rate limiting, input validation, HTTPS
- **PERFORMANT**: Efficient pagination, selective field expansion, proper caching

### Phase 9: Protocols & Transport
**Application Protocols:**
- **HTTP/HTTPS**: Standard web APIs (default)
- **WebSocket**: Real-time bidirectional (chat, collaboration)
- **gRPC**: High-performance internal services
- **AMQP**: Async messaging, decoupled systems

**Transport Layer:**
- **TCP**: Reliable, ordered, error-checked (default)
  - Use for: Web APIs, databases, email, file transfer
- **UDP**: Fast, lightweight, no guarantee
  - Use for: Video streaming, gaming, live streams

**Stateless by Default**: Make APIs stateless for easy horizontal scaling. Add state only when needed.

### Phase 10: Authentication vs Authorization
**AUTHENTICATION (Who ARE you?):**
- Basic Auth, Bearer Tokens, OAuth2 + JWT
- Access + Refresh tokens
- SSO (Single Sign-On)

**AUTHORIZATION (What can you DO?):**
- **RBAC**: Role-based (admin, editor, viewer)
- **ABAC**: Attribute-based (flexible, complex)
- **ACL**: Access Control Lists (per-resource permissions)

Real systems often COMBINE these models.

### Phase 11: Security by Design
Assume your system WILL be attacked. Design protection from day 1.

**Security Layers (Defense in Depth):**
1. **NETWORK**: Firewall, DDoS protection, VPN, private subnets
2. **TRANSPORT**: HTTPS/TLS for all communication
3. **APPLICATION**: Rate limiting, input validation, output encoding, CSRF tokens
4. **AUTHENTICATION**: Strong passwords, MFA, secure sessions, short-lived JWT
5. **AUTHORIZATION**: Least privilege, RBAC/ABAC, audit logs
6. **DATA**: Encryption at rest, encrypted backups, password hashing
7. **MONITORING**: Intrusion detection, anomaly detection, security audit logs

**Common Attacks + Prevention:**
| Attack | Prevention |
|--------|------------|
| SQL Injection | Parameterized queries |
| XSS | Output encoding, CSP headers |
| CSRF | CSRF tokens, SameSite cookies |
| DDoS | Rate limiting, CDN, cloud protection |
| Brute force | Rate limiting, account lockout, 2FA |
| Man-in-the-middle | HTTPS/TLS, certificate pinning |

## Quick Checklist

For ANY system design:
- ☐ Start with single server model
- ☐ Monitor and identify bottlenecks
- ☐ Separate concerns (web tier ↔ data tier)
- ☐ Choose database by asking questions (SQL vs NoSQL)
- ☐ Scale vertical first, then horizontal
- ☐ Add load balancer when horizontal scaling needed
- ☐ Eliminate single points of failure
- ☐ Design APIs as contracts (predictable, consistent, simple, secure, performant)
- ☐ Choose protocols based on interaction patterns
- ☐ Add authentication (who are you?) + authorization (what can you do?)
- ☐ Security by design (assume you'll be attacked)

## Use This Approach For
- Building from scratch with uncertain scale
- Rapid iteration needed
- Startup environments
- When you need to ship fast and evolve as you grow

## See Also
- `tech-stack`: For choosing the right technologies
- `approach-1-planned`: For comprehensive upfront planning
- `approach-3-comprehensive`: For complete curriculum learning
