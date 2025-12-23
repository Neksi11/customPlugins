# MongoDB Query Performance Guide

Strategies and techniques for optimizing MongoDB query performance.

## Index Fundamentals

### How Indexes Work

Indexes in MongoDB work like book indexes - they allow the database to find documents without scanning every document in a collection.

```javascript
// Before index: Collection scan (COLLSCAN)
db.users.find({ email: "user@example.com" }).explain("executionStats")
// executionTimeMillis: 5000

// After index: Index scan (IXSCAN)
db.users.createIndex({ email: 1 })
db.users.find({ email: "user@example.com" }).explain("executionStats")
// executionTimeMillis: 5
```

### ESR Rule (Equality, Sort, Range)

Order compound index fields for optimal performance:

1. **E** - Equality matches first
2. **S** - Sort fields next
3. **R** - Range filters last

```javascript
// Query: { status: "active" }
//        .sort({ createdAt: -1 })
//        .filter({ age: { $gte: 25 } })

// Optimal index order:
db.collection.createIndex({ status: 1, createdAt: -1, age: 1 })
```

### Index Types

| Index Type | Use Case | Syntax |
|------------|----------|--------|
| Single Field | Queries on one field | `{ field: 1 }` |
| Compound | Queries on multiple fields | `{ f1: 1, f2: -1 }` |
| Multikey | Array element queries | `{ tags: 1 }` |
| Text | Full-text search | `{ content: "text" }` |
| Geospatial | Location queries | `{ loc: "2dsphere" }` |
| Hashed | Hash-based sharding | `{ _id: "hashed" }` |
| Wildcard | Unknown field queries | `{ "$**": 1 }` |

## Query Analysis

### Using Explain

Analyze query execution with `explain()`:

```javascript
// Query plan only
db.collection.find({ field: value }).explain()

// Execution statistics
db.collection.find({ field: value }).explain("executionStats")

// All information
db.collection.find({ field: value }).explain("allPlansExecution")
```

### Key Metrics

Watch for these metrics in explain output:

```javascript
{
  "executionStats": {
    "executionSuccess": true,
    "executionTimeMillis": 15,       // Total execution time
    "totalDocsExamined": 100,        // Documents scanned
    "totalKeysExamined": 100,        // Index entries scanned
    "stage": "IXSCAN"                // COLLSCAN = bad, IXSCAN = good
  }
}
```

### Identifying Slow Queries

```javascript
// Get slow queries from profiler (must enable first)
db.setProfilingLevel(2, { slowms: 100 })  // Log queries >100ms
db.system.profile.find().sort({ ts: -1 }).limit(10)

// Check current operations
db.currentOp({ "command.$comment": "my-query" })
```

## Covered Queries

A query is "covered" when all fields are in the index - no document lookup needed.

```javascript
// Create compound index
db.products.createIndex({ category: 1, price: 1, name: 1 })

// Covered query - only uses index
db.products.find(
  { category: "electronics" },
  { category: 1, price: 1, name: 1, _id: 0 }
)

// Not covered - requires fetching document
db.products.find(
  { category: "electronics" },
  { category: 1, price: 1, description: 1, _id: 0 }
)
```

## Index Intersection

MongoDB can use multiple indexes for a single query:

```javascript
db.collection.createIndex({ status: 1 })
db.collection.createIndex({ createdAt: 1 })

// MongoDB may use both indexes
db.collection.find({ status: "active", createdAt: { $gte: date } })
```

**Tip:** Compound indexes are usually faster than index intersection.

## Pagination Strategies

### Avoid Large Skips

Skip-based pagination becomes slow with large offset values:

```javascript
// Bad for large collections
db.collection.find({}).skip(100000).limit(10)
// Scans and skips 100,000 documents!
```

### Use Range-Based Pagination

```javascript
// First page
db.collection.find({}).sort({ _id: 1 }).limit(10)

// Next page (use last _id from previous page)
db.collection.find({ _id: { $gt: lastId } }).sort({ _id: 1 }).limit(10)
```

### Use Seek Method with Compound Key

```javascript
// Create index on sort fields
db.collection.createIndex({ category: 1, _id: 1 })

// Paginate within category
db.collection.find({
  category: "electronics",
  _id: { $gt: lastId }
}).sort({ category: 1, _id: 1 }).limit(10)
```

## Sharding Considerations

### Choose Shard Key Carefully

```javascript
// Good shard keys have:
// 1. High cardinality (many unique values)
// 2. Even distribution (no hotspots)
// 3. Query locality (related data together)

sh.shardCollection("db.users", { region: 1, userId: 1 })
```

### Avoid Scatter-Gather Queries

```javascript
// Bad - queries all shards
db.users.find({ loginDate: { $gte: date } })

// Good - queries specific shard
db.users.find({ region: "us-east", userId: 12345 })
```

## Memory Optimization

### Working Set

Ensure your working set fits in RAM:

```javascript
// Check database stats
db.stats()

// Check collection stats
db.collection.stats()

// Working set ≈ data + indexes
```

### Index Size Management

```javascript
// Check index sizes
db.collection.aggregate([
  { $indexStats: {} }
])

// Sparse indexes (exclude documents where field doesn't exist)
db.collection.createIndex({ optional: 1 }, { sparse: true })

// Partial indexes (index only matching documents)
db.collection.createIndex(
  { status: 1 },
  { partialFilterExpression: { status: { $gt: 0 } } }
)
```

## Write Performance

### Bulk Operations

```javascript
// Use bulkWrite for multiple operations
db.collection.bulkWrite([
  { insertOne: { document: { ... } } },
  { updateOne: { filter: { _id: 1 }, update: { $set: { ... } } } },
  { deleteOne: { filter: { _id: 2 } } }
])
```

### Unordered Writes

```javascript
// Continue on error (faster for bulk loads)
db.collection.insertMany(docs, { ordered: false })
```

### Write Concern

```javascript
// Tunable write concern
db.collection.insertOne(
  doc,
  { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
)

// w: 0     - Fire and forget (fastest, no confirmation)
// w: 1     - Acknowledged (default)
// w: majority - Majority of replicas
// j: true  - Journal write acknowledged
```

## Common Performance Issues

### Missing Index

```javascript
// Symptom: COLLSCAN in explain output
// Solution: Create index on queried fields
db.collection.createIndex({ field: 1 })
```

### Too Many Indexes

```javascript
// Symptom: Slow writes, large storage overhead
// Solution: Remove unused indexes
db.collection.dropIndex("unused_index_1")
```

### Large Documents

```javascript
// Symptom: Slow queries despite index
// Solution: Use projection to limit returned fields
db.collection.find({ query }, { field1: 1, field2: 1 })
```

### In-Memory Sort

```javascript
// Symptom: "Sort exceeded memory limit"
// Solution: Index on sort fields
db.collection.createIndex({ field: 1 })
```

## Performance Checklist

- [ ] All queries use indexes (check explain output)
- [ ] Compound indexes follow ESR rule
- [ ] Working set fits in available RAM
- [ ] No large skip() values (>1000)
- [ ] Projection limits returned fields
- [ ] Covered queries where possible
- [ ] Appropriate write concern for operations
- [ ] Regular index maintenance (remove unused)
- [ ] Monitor query performance with profiler
- [ ] Schema design minimizes document growth
