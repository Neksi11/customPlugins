---
name: approach-1-planned
description: Approach 1: Planned Architecture (Bottom-Up Planning). Best for designing specific systems with known requirements. Follow the 7-step process: Requirements → Capacity Planning → Architecture → Flows → API → Data Layer → Scale Strategy.
version: 1.0.0
---

# Approach 1: Planned Architecture

## Overview
This approach follows a bottom-up, iterative methodology. Start by defining requirements, do the math for capacity planning, then design the complete architecture before coding.

## The 7-Step Process

### Step 1: Requirements Clarification
Define:
- **USERS**: Who? (Consumers, Creators, Admins)
- **SCALE**: How many? (Users, Items, Requests, Growth)
- **FEATURES**: What must it DO? (Core vs Nice-to-have)

### Step 2: Capacity Planning
For EACH major entity:
```
ENTITY    │ QUANTITY │ SIZE/UNIT │ TOTAL STORAGE
─────────┼──────────┼───────────┼──────────────
Users     │ 500K     │ 1 KB      │ 0.5 GB
Songs     │ 30M      │ 3 MB      │ 90 TB
Metadata  │ 30M      │ 100 B     │ 3 GB
```

**Key Question**: What dominates YOUR system?
- Storage-heavy? → Focus on object storage
- Compute-heavy? → Focus on scaling compute
- Read-heavy? → Focus on caching, replicas
- Write-heavy? → Focus on write optimization

### Step 3: High-Level Architecture
Draw the BIG picture - boxes and arrows:
```
CLIENTS → GATEWAY → APPLICATION LAYER → DATA LAYER
                       (stateless)    (SQL/NoSQL)
                                       Cache
                                       Storage
```

### Step 4: Design the Flows
Map EVERY major user interaction:

**READ FLOW**: User Action → Client Request → Gateway → Auth → App Layer → Query → Data → Return

**WRITE FLOW**: User Action → Client Request → Gateway → Auth + Permission → Validate → Process → Persist → Trigger side-effects

### Step 5: API & Interface Design
Define ALL endpoints/resources:
- `/songs` → Collection
- `/songs/{id}` → Specific item
- `/artists/{id}/songs` → Nested resource

Common patterns:
- `GET /{resource}` → List
- `GET /{resource}/{id}` → Get one
- `POST /{resource}` → Create
- `PATCH/PUT /{resource}/{id}` → Update
- `DELETE /{resource}/{id}` → Delete

### Step 6: Data Layer Design

**Storage Decision Tree:**
- Large files? (>1MB) → Object Storage (S3, Blob)
- Need complex queries/joins? → Relational (Postgres, MySQL)
- Flexible schema? → NoSQL (MongoDB, DynamoDB)
- Key-value only? → Redis, Memcached

**Schema Design:**
For EACH entity:
- What uniquely identifies it? → PRIMARY KEY
- What references other entities? → FOREIGN KEYS
- What will we search/filter by? → INDEXES
- What data is shared/related? → JOIN TABLES

### Step 7: Scale & Evolution Strategy
Start simple, scale WHEN needed:
- **Phase 1**: Single Region (1 LB, 2-3 App Servers, 1 DB, 1 Storage)
- **Phase 2**: Caching + Replicas (CDN, cache layer, read replicas)
- **Phase 3**: Multi-Region (regional LBs, storage, CDN edges)
- **Phase 4**: Sharding (by region/user_id)

**What to Scale When:**
- Slow page loads → Add CDN edge locations
- DB CPU at 100% → Add read replicas
- Too much DB write traffic → Leader-follower pattern
- Single DB too large → Shard by geography/user ID
- App servers overloaded → Horizontal scale
- Storage costs too high → Lifecycle policies, compression

## Quick Reference Questions

For ANY system design question, ask in THIS order:

1. **What problem are we solving?** (Requirements)
2. **How big is it?** (Capacity)
3. **What are the pieces?** (Architecture)
4. **How does data flow?** (Read/Write paths)
5. **How do we interact?** (API)
6. **Where does data live?** (Storage/Schema)
7. **What breaks first?** (Scale strategy)

## Use This Approach For
- Designing specific systems (e.g., Spotify clone)
- Known requirements and scale
- Enterprise systems
- When you have time to plan thoroughly

## See Also
- `tech-stack`: For choosing the right technologies
- `approach-2-evolutionary`: For starting simple and evolving
- `approach-3-comprehensive`: For complete curriculum learning
