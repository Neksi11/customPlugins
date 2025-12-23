---
name: mongodb-query-patterns
description: This skill should be used when the user asks to "query MongoDB", "find documents", "MongoDB query syntax", "filter MongoDB documents", "MongoDB operators", "project fields in MongoDB", or asks about MongoDB query performance, indexing strategies, or CRUD query patterns. Provides comprehensive MongoDB query guidance.
version: 1.0.0
---

# MongoDB Query Patterns

## Purpose

This skill provides comprehensive guidance for querying MongoDB databases effectively. Cover query syntax, filtering, projections, operators, and performance optimization strategies for MongoDB queries.

## When to Use

Activate this skill when working with MongoDB query operations including:
- Finding and filtering documents
- Using query operators ($gt, $lt, $in, $regex, etc.)
- Field projection and selection
- Query optimization and indexing
- Complex query patterns
- Geospatial queries
- Text search queries

## Core Query Concepts

### Basic Find Syntax

The foundation of MongoDB queries is the `find()` method:

```javascript
// Find all documents
db.collection.find()

// Find with equality filter
db.collection.find({ field: value })

// Find with multiple conditions
db.collection.find({ field1: value1, field2: value2 })
```

### Query Operators

MongoDB provides rich comparison operators:

```javascript
// Comparison operators
db.collection.find({ field: { $gt: 10 } })           // Greater than
db.collection.find({ field: { $gte: 10 } })          // Greater or equal
db.collection.find({ field: { $lt: 10 } })           // Less than
db.collection.find({ field: { $lte: 10 } })          // Less or equal
db.collection.find({ field: { $ne: 10 } })           // Not equal
db.collection.find({ field: { $in: [1, 2, 3] } })    // In array
db.collection.find({ field: { $nin: [1, 2, 3] } })   // Not in array
```

### Logical Operators

Combine conditions with logical operators:

```javascript
// $or - At least one condition must match
db.collection.find({
  $or: [
    { field1: value1 },
    { field2: value2 }
  ]
})

// $and - All conditions must match
db.collection.find({
  $and: [
    { field: { $gt: 10 } },
    { field: { $lt: 20 } }
  ]
})

// $not - Negates the query condition
db.collection.find({ field: { $not: { $gt: 10 } } })
```

### Field Projection

Control which fields are returned:

```javascript
// Include specific fields
db.collection.find({ query }, { field1: 1, field2: 1 })

// Exclude specific fields
db.collection.find({ query }, { field1: 0, field2: 0 })

// Exclude _id only
db.collection.find({ query }, { _id: 0 })

// Use projection with aggregation
db.collection.aggregate([
  { $match: { status: "active" } },
  { $project: { name: 1, email: 1, _id: 0 } }
])
```

### Array Queries

Query arrays and array elements:

```javascript
// Match exact array
db.collection.find({ tags: ["mongodb", "nodejs"] })

// Match array containing value
db.collection.find({ tags: "mongodb" })

// Match multiple values in array
db.collection.find({ tags: { $all: ["mongodb", "nodejs"] } })

// Query array by index
db.collection.find({ "items.0": "first-item" })

// Query array by size
db.collection.find({ tags: { $size: 3 } })
```

### Embedded Document Queries

Query nested documents:

```javascript
// Dot notation for nested fields
db.collection.find({ "address.city": "New York" })

// Query entire embedded document
db.collection.find({
  address: { street: "123 Main", city: "New York" }
})

// Query nested array elements
db.collection.find({ "comments.0.user": "alice" })
```

### Element Operators

Query by field existence and type:

```javascript
// Check field exists
db.collection.find({ field: { $exists: true } })

// Check field type (1=double, 2=string, 3=object, 4=array, etc.)
db.collection.find({ field: { $type: "string" } })
db.collection.find({ field: { $type: ["string", "null"] } })
```

### Regex Queries

Pattern matching with regex:

```javascript
// Case-sensitive regex
db.collection.find({ name: { $regex: "^John" } })

// Case-insensitive
db.collection.find({ name: { $regex: "^john", $options: "i" } })

// Contains pattern
db.collection.find({ email: { $regex: "@gmail\\.com$" } })
```

## Query Optimization

### Indexing Strategy

Effective indexing is crucial for query performance:

```javascript
// Create single field index
db.collection.createIndex({ field: 1 })

// Create compound index
db.collection.createIndex({ field1: 1, field2: -1 })

// Create text index for search
db.collection.createIndex({ content: "text" })

// Check index usage with explain
db.collection.find({ field: value }).explain("executionStats")
```

### Covered Queries

Create queries that are covered by indexes:

```javascript
// Create compound index
db.collection.createIndex({ status: 1, created: 1, name: 1 })

// Query covered by index (no document lookup needed)
db.collection.find(
  { status: "active" },
  { status: 1, created: 1, name: 1, _id: 0 }
)
```

### Query Performance Tips

1. **Use indexes**: Create indexes on frequently queried fields
2. **Limit results**: Use `limit()` to reduce data transfer
3. **Project fields**: Return only needed fields
4. **Avoid large skips**: Use range-based pagination instead
5. **Use `$in` wisely**: Limit array size in `$in` operators

## Common Query Patterns

### Pagination

```javascript
// Skip-based (not recommended for large skips)
db.collection.find({}).skip(20).limit(10)

// Range-based (recommended)
db.collection.find({ _id: { $gt: lastId } }).limit(10)
```

### Sorting

```javascript
// Ascending
db.collection.find({}).sort({ field: 1 })

// Descending
db.collection.find({}).sort({ field: -1 })

// Compound sort
db.collection.find({}).sort({ field1: 1, field2: -1 })
```

### Counting

```javascript
// Count all matching documents
db.collection.countDocuments({ status: "active" })

// Estimated count (faster, less accurate)
db.collection.estimatedDocumentCount()
```

### Distinct Values

```javascript
// Get unique values for a field
db.collection.distinct("category", { active: true })
```

## Additional Resources

### Reference Files

For detailed operator documentation and advanced patterns:
- **`references/operators.md`** - Complete operator reference
- **`references/performance.md`** - Performance optimization guide
- **`references/geospatial.md`** - Geospatial query patterns

### Example Files

Working examples in `examples/`:
- **`basic-queries.js`** - Common query patterns
- **`advanced-filters.js`** - Complex filter examples
- **`array-queries.js`** - Array query patterns

### Scripts

Utility scripts in `scripts/`:
- **`query-builder.py`** - Build MongoDB queries programmatically
- **`index-analyzer.js`** - Analyze query index usage
