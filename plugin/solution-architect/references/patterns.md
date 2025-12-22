# Problem Patterns Reference

Common problem patterns and their typical solution approaches. Used for quickly identifying solution types based on problem characteristics.

## Pattern Categories

### Automation Patterns
Problems solved by connecting systems and automating workflows.

### API Patterns
Problems requiring programmatic access to data or functionality.

### Data Processing Patterns
Problems involving transformation, analysis, or movement of data.

### User Interface Patterns
Problems requiring human-facing interfaces.

### Integration Patterns
Problems connecting existing systems together.

---

## Automation Patterns

### Pattern: Email/Notification Automation
**Trigger:** New event occurs → Send notification
**Characteristics:**
- Event-driven
- One-to-many or one-to-one communication
- Template-based messages

**Solution Approaches (in order of preference):**
1. **n8n/Zapier/Make** - If connecting existing SaaS
2. **Backend API + Queue** - If custom logic needed
3. **Serverless functions** - If spiky volume

**Key Considerations:**
- Email provider needed (SendGrid, AWS SES, Resend)
- Rate limits and deliverability
- Template management
- Unsubscribe handling

---

### Pattern: Data Synchronization
**Trigger:** Data changes in System A → Sync to System B
**Characteristics:**
- Periodic or real-time sync
- Data transformation may be needed
- Error handling critical

**Solution Approaches:**
1. **n8n/Make** - For simple 1:1 syncs
2. **Backend API + Cron** - For complex transformations
3. **Serverless + Webhooks** - For real-time sync

**Key Considerations:**
- Idempotency (handle duplicate syncs)
- Conflict resolution
- Error recovery and retry logic
- Data volume and frequency

---

### Pattern: Approval Workflow
**Trigger:** Request → Human Approval → Action
**Characteristics:**
- Multi-step workflow
- Human decision points
- State tracking needed

**Solution Approaches:**
1. **n8n/Make** - Visual workflow builder
2. **Low-code platform** (Airtable, Notion) - For business users
3. **Backend + State Machine** - For complex logic

**Key Considerations:**
- State management (pending, approved, rejected)
- Notification of approvers
- Timeout handling
- Audit trail

---

## API Patterns

### Pattern: CRUD API
**Trigger:** Client needs to Create, Read, Update, Delete resources
**Characteristics:**
- Standard data operations
- Multiple clients (web, mobile)
- Authentication needed

**Solution Approaches:**
1. **Backend API** (Express/Fastify/FastAPI) - Standard choice
2. **Serverless functions** - If low volume or spiky traffic
3. **BaaS** (Supabase, Firebase) - For fastest development

**Key Considerations:**
- Framework choice based on team skills
- Database (PostgreSQL for relational, MongoDB for flexible)
- Authentication (JWT, sessions, OAuth)
- Validation (Zod, Pydantic, Joi)

---

### Pattern: Webhook Handler
**Trigger:** External service sends webhook → Process and respond
**Characteristics:**
- External system initiates
- Need to respond quickly
- Idempotency important

**Solution Approaches:**
1. **Serverless function** - Perfect fit
2. **Backend API endpoint** - If complex processing needed
3. **n8n webhook node** - For simple processing

**Key Considerations:**
- Quick response (<3 seconds)
- Idempotency (retry handling)
- Signature verification
- Async processing for long tasks

---

### Pattern: Real-time API
**Trigger:** Multiple parties need simultaneous updates
**Characteristics:**
- Bidirectional communication
- Low latency required
- Connection management

**Solution Approaches:**
1. **WebSocket** (Backend API) - Standard approach
2. **Serverless WebSocket** (AWS API Gateway) - For scale
3. **SSE** (Server-Sent Events) - For one-way updates

**Key Considerations:**
- Connection state management
- Reconnection logic
- Scaling WebSocket connections
- Message ordering

---

## Data Processing Patterns

### Pattern: ETL (Extract, Transform, Load)
**Trigger:** Move data from source to destination with transformation
**Characteristics:**
- Batch processing
- Data transformation
- Error handling critical

**Solution Approaches:**
1. **Python script** - For one-time or simple ETL
2. **n8n** - For visual ETL workflows
3. **Backend + Queue** - For complex, reliable ETL

**Key Considerations:**
- Data volume (memory constraints)
- Error logging and recovery
- Idempotency (re-run safely)
- Data validation

---

### Pattern: Stream Processing
**Trigger:** Continuous data flow needs processing
**Characteristics:**
- Real-time or near-real-time
- Unbounded data stream
- State may be needed

**Solution Approaches:**
1. **Serverless + Stream** - AWS Lambda + Kinesis
2. **Backend + WebSocket** - For client-facing streams
3. **Stream processing framework** - For complex needs (Kafka Streams)

**Key Considerations:**
- Backpressure handling
- State management
- Order guarantee
- Fault tolerance

---

### Pattern: Batch Processing
**Trigger:** Process large datasets periodically
**Characteristics:**
- Scheduled execution
- Large data volumes
- Progress tracking helpful

**Solution Approaches:**
1. **Cron job** - Simplest for single machine
2. **Serverless scheduled** - For cloud-native approach
3. **Queue + Workers** - For reliable, scalable processing

**Key Considerations:**
- Resource management (memory, CPU)
- Checkpointing (resume if fails)
- Parallelization opportunities
- Job monitoring

---

## User Interface Patterns

### Pattern: Admin Dashboard
**Trigger:** Internal team needs to manage data
**Characteristics:**
- CRUD operations
- Authentication required
- Internal users only

**Solution Approaches:**
1. **Low-code platform** (Airtable, Knack) - Fastest
2. **Backend + Admin UI** (React Admin, Django Admin) - For customization
3. **n8n + Simple frontend** - For workflow-based admin

**Key Considerations:**
- User permissions (roles, access control)
- Audit logging
- Bulk operations
- Export capabilities

---

### Pattern: Customer Portal
**Trigger:** External users need self-service access
**Characteristics:**
- Public-facing
- Authentication required
- Polished UI needed

**Solution Approaches:**
1. **Next.js + Backend API** - Modern, SEO-friendly
2. **Vue + Backend** - Progressive framework
3. **SaaS** (MemberStack, etc.) - For simple portals

**Key Considerations:**
- Authentication (JWT, OAuth, magic links)
- Responsive design
- Performance (loading states, caching)
- Accessibility

---

### Pattern: Mobile App Backend
**Trigger:** Mobile app needs data and authentication
**Characteristics:**
- REST or GraphQL API
- Push notifications
- Offline sync consideration

**Solution Approaches:**
1. **Backend API + Push service** - Custom backend
2. **BaaS** (Supabase, Firebase) - For fastest development
3. **GraphQL + Subscriptions** - For real-time features

**Key Considerations:**
- API design (mobile-friendly responses)
- Authentication (token refresh)
- Data synchronization
- Push notification provider

---

## Integration Patterns

### Pattern: Third-party API Integration
**Trigger:** Need to work with external service's API
**Characteristics:**
- API client implementation
- Rate limiting
- Error handling

**Solution Approaches:**
1. **Backend API** - Wraps third-party API
2. **n8n** - For simple integrations without code
3. **Serverless** - For sporadic usage

**Key Considerations:**
- Rate limit handling
- Retry logic with exponential backoff
- Caching for expensive calls
- API version management

---

### Pattern: Legacy System Integration
**Trigger:** Modern system needs to talk to legacy system
**Characteristics:**
- Old technology stack
- Limited API capabilities
- May require file-based integration

**Solution Approaches:**
1. **Backend API + Adapter** - Abstraction layer
2. **Message queue** - Decoupled integration
3. **ETL jobs** - For file-based sync

**Key Considerations:**
- Data format transformation
- Error handling and logging
- Monitoring legacy system health
- Gradual migration path

---

## Quick Pattern Identifier

Use this to quickly identify the pattern and suggested approach:

```
Is this about connecting systems?
├─ Yes → Automation or Integration Pattern
│  ├─ Is there human approval needed?
│  │  ├─ Yes → Approval Workflow → n8n/Make
│  │  └─ No → Data Sync or Trigger-Action
│  │     ├─ Real-time? → Webhook Handler or Backend
│  │     └─ Scheduled? → n8n or Cron + Backend
│  └─ Legacy system involved?
│     └─ Legacy Integration → Backend + Adapter
└─ No → Is this about data?
   ├─ Yes → Data Processing Pattern
   │  ├─ One-time/large volume? → ETL → Script or Backend
   │  ├─ Continuous/streaming? → Stream Processing → Backend or Serverless
   │  └─ Scheduled batch? → Batch Processing → Cron or Queue
   └─ No → Is this about users?
      ├─ Internal admin? → Admin Dashboard → Low-code or Backend + Admin UI
      ├─ External customers? → Customer Portal → Next.js/Vue + Backend
      └─ Mobile app? → Mobile Backend → Backend API or BaaS
```

---

Update this reference when new patterns are identified or existing patterns need refinement.
