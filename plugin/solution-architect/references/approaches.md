# Solution Approaches Reference

Detailed reference information for common solution approaches. Used by commands, skills, and agents to provide consistent, accurate guidance.

## n8n / Workflow Automation

### Overview
Node-based workflow automation platform for self-hosted or cloud-based automation.

### Best For
- Quick integrations between SaaS products
- Business process automation (approvals, notifications, data sync)
- API orchestration without writing code
- Teams wanting visual, maintainable workflows

### Avoid If
- Complex custom business logic
- High-frequency execution (>50k runs/month)
- Need sub-second response times
- Require extensive custom code

### Characteristics
| Aspect | Details |
|--------|---------|
| **Complexity** | Low (visual workflows) |
| **Build Time** | 1-3 days for typical workflow |
| **Monthly Cost** | Free (self-hosted) or $20-80 (cloud) |
| **Max Scale** | ~50k workflow runs/month |
| **Skills Needed** | Low (no code required) |
| **Maintenance** | Visual (easy for non-developers) |

### Pros
- Self-hosted option (no vendor lock-in)
- 200+ app integrations
- Visual debugging
- JavaScript code nodes for custom logic
- Active community and documentation

### Cons
- Execution limits on cloud
- Limited for complex business logic
- Visual workflows can become complex
- Less control than code

### Outgrow Signals
- More than 100 workflow nodes
- Complex JavaScript in code nodes
- Need <1 second response times
- >50k executions per month

### Migration Path
When outgrowing n8n:
1. Extract business logic from code nodes → service layer
2. Replace workflow nodes → API endpoints
3. Replace triggers → webhooks/event system
4. Implement scheduled tasks → cron/queue workers

---

## Backend API (Express/Fastify/etc.)

### Overview
Traditional backend service exposing HTTP endpoints for data operations and business logic.

### Best For
- Custom business logic
- APIs consumed by web/mobile apps
- Complex data processing
- Full control over behavior

### Avoid If
- Simple integrations would suffice
- Team lacks backend development skills
- Timeline is very tight (<1 week)
- Just need to connect existing services

### Characteristics
| Aspect | Details |
|--------|---------|
| **Complexity** | Medium-High |
| **Build Time** | 1-3 weeks for typical API |
| **Monthly Cost** | $5-100 (hosting) |
| **Max Scale** | ~100k users with optimization |
| **Skills Needed** | High (backend development) |
| **Maintenance** | Code (requires developer) |

### Framework Comparison

| Framework | Language | Best For | Build Time |
|-----------|----------|----------|------------|
| Express | JavaScript | Quick APIs, flexibility | 1-2 weeks |
| Fastify | JavaScript | Performance, TypeScript | 1-2 weeks |
| FastAPI | Python | Auto-docs, async | 1-2 weeks |
| Django | Python | Full-featured, rapid | 1-3 weeks |
| NestJS | TypeScript | Enterprise, structured | 2-4 weeks |

### Pros
- Complete control over behavior
- Scalable to high loads
- Rich ecosystem of libraries
- Industry-standard approach
- Can optimize for specific needs

### Cons
- Higher development cost
- Requires backend skills
- More operational complexity
- Longer time to first value
- Security implementation required

### Common Components
- **Routes/Controllers**: HTTP endpoints
- **Services**: Business logic layer
- **Models/ORM**: Data access layer
- **Middleware**: Auth, validation, logging
- **Database**: PostgreSQL, MongoDB, etc.

---

## Serverless Functions

### Overview
Individual functions executed on demand, paying only for actual usage.

### Best For
- Spiky/unknown traffic patterns
- Event-driven architectures
- Simple, isolated operations
- Pay-per-use desired

### Avoid If
- Consistent high load (reserved instances cheaper)
- Long-running processes (>15 min)
- Complex inter-function communication
- Need sub-100ms cold starts

### Characteristics
| Aspect | Details |
|--------|---------|
| **Complexity** | Medium |
| **Build Time** | 2-5 days for typical function set |
| **Monthly Cost** | $0-50 (pay-per-use) |
| **Max Scale** | Virtually unlimited |
| **Skills Needed** | Medium (cloud + code) |
| **Maintenance** | Low (platform manages infra) |

### Platform Comparison

| Platform | Language | Cold Start | Free Tier |
|----------|----------|------------|-----------|
| AWS Lambda | Many | ~500ms | 1M requests/month |
| Vercel Functions | Node.js | ~100ms | 100k GB-hours |
| Cloud Functions | Node/Python/Go | ~500ms | 2M invocations |
| Netlify Functions | Node.js | ~200ms | 125k functions/month |

### Pros
- Pay only for usage
- Auto-scaling
- No server management
- Easy to deploy
- Built-in monitoring

### Cons
- Cold start delays
- Vendor lock-in risk
- Harder to test locally
- 15-minute execution limit
- Debugging complexity

### Common Patterns
- **Webhook handlers**: Respond to webhooks
- **Scheduled tasks**: Cron-triggered functions
- **API endpoints**: HTTP-triggered functions
- **Data processors**: File upload/stream processing
- **Event handlers**: Database/pubsub triggers

---

## Scripting (Python/Bash/Node.js)

### Overview
Simple scripts for automation, data processing, or one-off tasks.

### Best For
- One-time tasks or migrations
- Scheduled cron jobs
- Data processing and transformation
- Simple automation without UI

### Avoid If
- Need API or UI
- Complex error handling required
- Multiple users/actors
- Need to scale horizontally

### Characteristics
| Aspect | Details |
|--------|---------|
| **Complexity** | Low-Medium |
| **Build Time** | 1-5 days |
| **Monthly Cost** | $0-10 (hosting) |
| **Max Scale** | ~1k executions |
| **Skills Needed** | Medium (scripting language) |
| **Maintenance** | Code (requires developer) |

### Language Comparison

| Language | Best For | Ecosystem |
|----------|----------|-----------|
| Python | Data processing, ML, web scraping | Pandas, Requests, BeautifulSoup |
| Bash | System admin, file operations | Standard Unix tools |
| Node.js | JSON/API heavy tasks | Axios, Cheerio, FS |

### Pros
- Fast to write
- Full programming power
- No platform limitations
- Easy to version control
- Can run anywhere

### Cons
- No built-in UI
- Manual deployment
- Limited monitoring
- Requires scripting skills
- Doesn't scale automatically

### Common Use Cases
- **Data migration**: Transform and move data
- **Scheduled jobs**: Cron-based tasks
- **Web scraping**: Extract data from websites
- **File processing**: Transform files
- **API automation**: Call APIs in sequence

---

## SaaS Integration (Existing Tools)

### Overview
Using existing SaaS products instead of building custom solutions.

### Best For
- Common problems already solved
- Want fastest time to value
- No technical team
- Focus on core business, not infrastructure

### Avoid If
- Custom business logic is critical
- Need competitive differentiation
- SaaS cost exceeds build cost
- Require deep customization

### Characteristics
| Aspect | Details |
|--------|---------|
| **Complexity** | Very Low |
| **Build Time** | Hours to days |
| **Monthly Cost** | $50-500+ |
| **Max Scale** | Whatever SaaS offers |
| **Skills Needed** | None (configuration) |
| **Maintenance** | None (SaaS handles) |

### Common SaaS Categories

| Category | Examples | When to Use |
|----------|----------|-------------|
| Forms | Typeform, Airtable | Simple data collection |
| CMS | WordPress, Contentful | Content-heavy sites |
| E-commerce | Shopify, Stripe | Online stores |
| Auth | Auth0, Clerk | User management |
| Analytics | Mixpanel, PostHog | Event tracking |
| Email | SendGrid, Mailchimp | Email campaigns |
| Storage | AWS S3, Cloudinary | File hosting |

### Pros
- Fastest time to value
- No maintenance
- Continuous improvements from vendor
- Enterprise features available
- Support and documentation

### Cons
- Ongoing monthly cost
- Limited customization
- Vendor lock-in
- Data portability concerns
- Limited control

### Buy vs Build Framework

**Buy (Use SaaS) if:**
- It's not your core competency
- Multiple good options exist
- Cost < 3x monthly build cost
- Team lacks specific expertise
- Time to market is critical

**Build if:**
- It's your core differentiator
- No existing tool fits well
- Long-term cost favors building
- You need deep customization
- You have the expertise and time

---

## Decision Matrix Quick Reference

| Scenario | Recommended Approach |
|----------|---------------------|
| Connect 3 SaaS products | n8n / Zapier / Make |
| Custom business logic | Backend API |
| Event-driven, spiky traffic | Serverless |
| One-time data task | Scripting |
| Common problem (auth, forms) | SaaS |
| Real-time communication | WebSocket (Backend) |
| Mobile app backend | Backend API + BaaS |
| Internal admin tool | Low-code platform |
| Public API product | Backend API |
| Simple scheduled task | Cron script |
| Complex data pipeline | Backend + Queue |

---

This reference provides consistent information across all plugin components. Update when adding new approaches or updating existing guidance.
