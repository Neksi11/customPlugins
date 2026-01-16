---
name: tech-stack
description: Technology stack selection guide. Choose the right technologies for each system layer based on 5 dimensions: Requirements, Team Capability, Operational Cost, Ecosystem Maturity, and Scalability Path. All approaches reference this for technology decisions.
version: 1.0.0
---

# Tech Stack Selection Guide

## Overview
Never choose tech based on hype. Choose based on REQUIREMENTS. This guide provides decision trees and recommendations for every layer of the system stack.

## The 5 Dimensions of Choice

For EVERY technology decision, evaluate:

1. **REQUIREMENTS** - What does the system NEED to do?
   - Traffic volume, data characteristics, latency, consistency

2. **TEAM CAPABILITY** - What can we ACTUALLY build?
   - Existing skills, hiring market, learning curve

3. **OPERATIONAL COST** - What will it cost to RUN?
   - Cloud costs, maintenance overhead, complexity

4. **ECOSYSTEM MATURITY** - What SUPPORT exists?
   - Library availability, community size, long-term viability

5. **SCALABILITY PATH** - How does it GROW?
   - Horizontal scaling, vendor lock-in, bottlenecks

**WEIGHTING:** Requirements > Team > Operations > Ecosystem > Scalability
(You can scale later, but you can't fix wrong requirements or wrong team)

## Layer-by-Layer Decision Trees

### LAYER 1: Frontend (Client Apps)

```
What platforms do you need?
    │
    ├── iOS + Android ──► Cross-platform (React Native, Flutter) OR Native (Swift/Kotlin)
    │
    ├── Web only ────────► React/Next.js OR Vue/Nuxt
    │
    └── All platforms ───► React (web) + React Native (mobile) OR Flutter (all)
```

**RECOMMENDATION for Music Streaming:**
- **MOBILE**: React Native (cross-platform, large ecosystem) OR native for max audio performance
- **WEB**: React/Next.js (SSR for SEO, fast initial load)

### LAYER 2: Backend API

```
Team knows best?
    │
    ├── Python ──► FastAPI (async, fast) OR Flask (simple)
    │
    ├── JavaScript ─► Node.js + Express OR NestJS (structured)
    │
    ├── Java ──────► Spring Boot (enterprise, structured)
    │
    ├── Go ────────► Gin OR Echo (fast, low resource usage)
    │
    └── Other ─────► Use what you know, then optimize later
```

**Framework Comparison:**
| Framework | Perf | Ecosystem | Learning | Best For |
|-----------|------|------------|----------|----------|
| FastAPI | ★★★★★ | ★★★★☆ | ★★★☆☆ | Quick APIs, Python team |
| NestJS | ★★★★☆ | ★★★★★ | ★★☆☆☆ | Large teams, structure |
| Spring | ★★★★☆ | ★★★★★ | ★☆☆☆☆ | Enterprise, Java teams |
| Go (Gin) | ★★★★★ | ★★★☆☆ | ★★☆☆☆ | Maximum performance, simple |

**RECOMMENDATION for Music Streaming:**
- **FastAPI (Python)** - if team knows Python
- **Go + Gin** - if you need maximum performance
- **Node.js + NestJS** - if team is JavaScript-heavy

**START with what you know. OPTIMIZE later.**

### LAYER 3: Database (Metadata)

```
Large files? (>1MB per item)
    │
    ├── Yes ──► Object Storage (S3, Blob)
    │
    └── No ────┐
              ▼
        Need ACID transactions?
        │
        ├── Yes ──► SQL (PostgreSQL, MySQL)
        │
        └── No ────┐
                  ▼
            Schema changes frequently?
            │
            ├── Yes ──► NoSQL (MongoDB)
            │
            └── No ──► SQL (still better)
```

**PostgreSQL vs MySQL:**
| PostgreSQL | MySQL |
|------------|-------|
| Advanced features | Simpler setup |
| Better JSON support | Faster reads (sometimes) |
| Stronger data integrity | Larger community |
| Open source (no owner) | Oracle-owned |

**RECOMMENDATION:** PostgreSQL (more future-proof, better features)

### LAYER 4: Object Storage (Audio Files)

**Decision:** Use your cloud provider's native object storage

**Cloud Provider → Storage Service:**
- AWS → S3
- Azure → Blob Storage
- GCP → Cloud Storage
- Multi-cloud → MinIO (self-hosted)

**Key FEATURES NEEDED:**
- Presigned URLs (temporary access)
- Lifecycle policies (auto-delete old files)
- CDN integration
- Versioning (for artist re-uploads)

**File Organization:**
```
s3://music-platform-bucket/
  ├── audio/
  │   └── {song_id}/
  │       ├── 64kbps.opus
  │       ├── 128kbps.opus
  │       └── 320kbps.opus
  ├── images/
  │   ├── artists/{artist_id}.jpg
  │   └── albums/{album_id}.jpg
  └── uploads/
      └── {upload_id}.{ext}
```

### LAYER 5: Caching Layer

```
Do you NEED a cache?
    │
    ├── Read-heavy workload (90%+ reads) ──► YES
    ├── Expensive computations ────────────────► YES
    ├── High database CPU ─────────────────────► YES
    │
    └── Start small, add when needed ────────────► LATER
```

**CACHE OPTIONS:**
| Option | Use Case | Setup Difficulty |
|--------|----------|-------------------|
| Redis | General purpose, flexible | ★★☆☆☆ |
| Memcached | Simple caching only | ★☆☆☆☆ |
| In-app cache | Small datasets, simple | ★☆☆☆☆ |
| CDN cache | Static content, API responses | ★★★☆☆ |

**RECOMMENDATION:** Redis (most flexible, widely adopted)

**WHAT TO CACHE:**
- Song metadata (TTL: 1 hour)
- User playlists (TTL: 15 minutes)
- Trending songs (TTL: 30 minutes)
- Search results (TTL: 5 minutes)
- Session tokens (TTL: 24 hours)

### LAYER 6: CDN (Content Delivery Network)

```
Do you NEED a CDN?
    │
    ├── Global user base ──────────────────────► YES
    ├── Large static assets ────────────────────► YES
    ├── API response caching needed ─────────────► YES
    │
    └── Single region, small scale ──────────────► LATER
```

**CDN OPTIONS:**
| Provider | Best For | Global Reach |
|----------|----------|---------------|
| Cloudflare | Easy setup, DDoS protection | ★★★★★ |
| AWS CloudFront | AWS ecosystem | ★★★★☆ |
| Azure CDN | Azure ecosystem | ★★★★☆ |
| Fastly | Advanced caching features | ★★★★☆ |

**RECOMMENDATION:** Start with your cloud's CDN, add Cloudflare later

### LAYER 7: Message Queue (Async Operations)

```
Do you NEED a message queue?
    │
    ├── Background processing needed ────────► YES
    ├── Decoupling services ───────────────────► YES
    ├── Retry logic needed ────────────────────► YES
    │
    └── Simple sync operations ────────────────► LATER
```

**MESSAGE QUEUE OPTIONS:**
| Option | Best For | Complexity |
|--------|----------|-------------|
| RabbitMQ | Complex routing, reliability | ★★★☆☆ |
| Redis (Streams) | Simple queues, already have Redis | ★★☆☆☆ |
| AWS SQS | AWS ecosystem, simple | ★★☆☆☆ |
| Kafka | Event streaming, high volume | ★★★★★ |

**RECOMMENDATION:** Start with Redis (if you have it) or SQS

### LAYER 8: Load Balancer

```
What are your traffic patterns?
    │
    ├── Equal servers, stateless ──────────► Round Robin
    │
    ├── Variable session lengths ────────────► Least Connections
    │
    ├── Performance critical, different servers → Least Response Time
    │
    ├── Session affinity needed ──────────────► IP Hash
    │
    ├── Different server capacities ────────────► Weighted
    │
    ├── Global services, latency matters ───────► Geographic
    │
    └── Caching systems, distributed caches ────► Consistent Hashing
```

**LOAD BALANCER OPTIONS:**
| Option | Best For | Cost |
|--------|----------|------|
| AWS ALB | AWS ecosystem, layer 7 | Pay per request |
| Nginx | Self-hosted, configurable | Server cost |
| HAProxy | High performance, TCP/HTTP | Server cost |
| Cloudflare | DDoS protection, global | Free tier |

**RECOMMENDATION:** Use your cloud's load balancer (ALB/GCP/Azure)

## Recommended Stack for Spotify-Like System

| LAYER | CHOICE | WHY? |
|-------|--------|------|
| Mobile | React Native | Cross-platform, large ecosystem |
| Web | React/Next.js | SSR for SEO, fast development |
| Backend API | FastAPI (Python) | Async, fast, easy to learn |
| Database | PostgreSQL | ACID, joins, mature |
| Object Storage | AWS S3 | Scalable, CDN integration |
| Cache | Redis | Flexible, widely used |
| Message Queue | RabbitMQ/SQS | Async processing |
| Load Balancer | AWS ALB | Managed, health checks |
| CDN | CloudFront | AWS integration, global |
| Monitoring | Prometheus/Grafana | Open source, flexible |
| CI/CD | GitHub Actions | Integrated, free tier |

## Cost Estimation (Monthly, 500K users)

| Service | Monthly Cost |
|---------|--------------|
| EC2 (3 t3.medium) | $100 |
| RDS PostgreSQL (db.t3.large) | $150 |
| ElastiCache Redis | $80 |
| S3 Storage (100 TB) | $2,300 |
| CloudFront (10 TB transfer) | $850 |
| ALB | $20 |
| Domain + SSL | $15 |
| Monitoring (basic) | $0 (open source) |
| **TOTAL** | **~$3,500/month** |

## Alternative Stacks (by Team Expertise)

### JavaScript/TypeScript Teams
- Frontend: React (web) + React Native (mobile)
- Backend: Node.js + NestJS
- Database: PostgreSQL
- Cache: Redis
- Queue: BullMQ (Redis-based) or AWS SQS

### Enterprise/Java Teams
- Frontend: React (web) + Native Android/iOS
- Backend: Java + Spring Boot
- Database: PostgreSQL
- Cache: Redis
- Queue: RabbitMQ or AWS SQS

### Go/Performance Teams
- Frontend: React (web) + Flutter (mobile)
- Backend: Go + Gin
- Database: PostgreSQL
- Cache: Redis
- Queue: NATS or RabbitMQ

## Final Checklist

Before you start building:
- ☐ Does your team know the chosen languages?
- ☐ Can you hire people who know this stack?
- ☐ Have you estimated the monthly costs?
- ☐ Do you have a scaling plan for when you hit limits?
- ☐ Have you set up monitoring from day 1?
- ☐ Do you have a backup/disaster recovery plan?

**Remember:** The best stack is the one your team can actually build. Don't choose based on hype. Choose based on requirements.

## See Also
- `approach-1-planned`: For requirements-driven design
- `approach-2-evolutionary`: For bottleneck-driven evolution
- `approach-3-comprehensive`: For complete learning curriculum
