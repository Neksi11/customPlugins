---
name: mongodb-aggregations
description: This skill should be used when the user asks to "aggregate MongoDB", "MongoDB aggregation pipeline", "$group", "$match", "$lookup", "MongoDB aggregation stages", "aggregate data", "calculate statistics", or asks about MongoDB aggregation performance, pipeline optimization, or complex data transformations. Provides comprehensive MongoDB aggregation guidance.
version: 1.0.0
---

# MongoDB Aggregation Pipelines

## Purpose

This skill provides comprehensive guidance for building effective MongoDB aggregation pipelines. Cover all pipeline stages, optimization strategies, and common patterns for data transformation and analysis.

## When to Use

Activate this skill when working with MongoDB aggregation operations including:
- Building aggregation pipelines
- Data transformation and reshaping
- Statistical calculations and analytics
- Joining collections with $lookup
- Grouping and data aggregation
- Pipeline optimization strategies
- Complex multi-stage operations

## Aggregation Fundamentals

### Basic Pipeline Structure

Aggregation operations process documents through a pipeline of stages:

```javascript
db.collection.aggregate([
  { $match: { status: "active" } },     // Stage 1: Filter
  { $group: { _id: "$category" } },     // Stage 2: Group
  { $sort: { count: -1 } }              // Stage 3: Sort
])
```

### Pipeline Execution Order

MongoDB processes documents sequentially through stages:

1. **Early filtering**: Use `$match` early to reduce documents
2. **Projection**: Use `$project` to limit fields passed to next stage
3. **Grouping**: `$group` performs aggregation calculations
4. **Sorting**: `$sort` orders results
5. **Limiting**: `$limit` restricts output size

### Key Optimization Principle

**Filter early, project often**: Place `$match` as early as possible to minimize documents processed by subsequent stages.

## Core Pipeline Stages

### $match - Filter Documents

Filter documents before aggregation:

```javascript
// Single condition
db.sales.aggregate([
  { $match: { status: "completed" } }
])

// Multiple conditions
db.sales.aggregate([
  { $match: {
    status: "completed",
    date: { $gte: ISODate("2024-01-01") }
  }}
])

// With query operators
db.sales.aggregate([
  { $match: {
    amount: { $gt: 100 },
    region: { $in: ["US", "CA"] }
  }}
])
```

### $group - Aggregate Documents

Group documents and calculate aggregations:

```javascript
// Group by single field
db.sales.aggregate([
  { $group: {
    _id: "$category",
    total: { $sum: "$amount" },
    count: { $sum: 1 },
    avg: { $avg: "$amount" }
  }}
])

// Group by multiple fields
db.sales.aggregate([
  { $group: {
    _id: { category: "$category", region: "$region" },
    total: { $sum: "$amount" }
  }}
])

// Group with null (whole collection)
db.sales.aggregate([
  { $group: {
    _id: null,
    totalRevenue: { $sum: "$amount" },
    avgOrderValue: { $avg: "$amount" },
    totalOrders: { $sum: 1 }
  }}
])
```

### $project - Reshape Documents

Transform and shape documents:

```javascript
// Include specific fields
db.users.aggregate([
  { $project: {
    name: 1,
    email: 1,
    _id: 0
  }}
])

// Rename and compute fields
db.orders.aggregate([
  { $project: {
    orderId: "$_id",
    total: { $add: ["$subtotal", "$tax"] },
    year: { $year: "$createdAt" }
  }}
])

// Conditional projection
db.products.aggregate([
  { $project: {
    name: 1,
    price: 1,
    status: {
      $cond: [
        { $gt: ["$quantity", 0] },
        "in-stock",
        "out-of-stock"
      ]
    }
  }}
])
```

### $lookup - Join Collections

Perform left outer join:

```javascript
// Simple lookup
db.orders.aggregate([
  { $lookup: {
    from: "customers",
    localField: "customerId",
    foreignField: "_id",
    as: "customer"
  }}
])

// Lookup with array unwinding
db.orders.aggregate([
  { $lookup: {
    from: "products",
    localField: "items.productId",
    foreignField: "_id",
    as: "productDetails"
  }},
  { $unwind: "$productDetails" }
])

// Lookup with pipeline (MongoDB 5.0+)
db.orders.aggregate([
  { $lookup: {
    from: "customers",
    let: { customerId: "$customerId" },
    pipeline: [
      { $match: {
        $expr: { $eq: ["$_id", "$$customerId"] }
      }},
      { $project: { name: 1, email: 1 } }
    ],
    as: "customer"
  }}
])
```

### $unwind - Decompose Arrays

Split array elements into separate documents:

```javascript
// Unwind array field
db.posts.aggregate([
  { $unwind: "$tags" }
])

// Unwind with index preservation
db.posts.aggregate([
  { $unwind: {
    path: "$comments",
    includeArrayIndex: "commentIndex"
  }}
])

// Preserve empty/null arrays
db.posts.aggregate([
  { $unwind: {
    path: "$tags",
    preserveNullAndEmptyArrays: true
  }}
])
```

## Aggregation Operators

### Arithmetic Operators

```javascript
{ $add: [<expression1>, <expression2>, ...] }
{ $subtract: [<expression1>, <expression2>] }
{ $multiply: [<expression1>, <expression2>, ...] }
{ $divide: [<expression1>, <expression2>] }
{ $mod: [<expression1>, <expression2>] }
{ $abs: <number> }
{ $ceil: <number> }
{ $floor: <number> }
{ $ln: <number> }
{ $log: [<number>, <base>] }
{ $log10: <number> }
{ $pow: [<number>, <exponent>] }
{ $sqrt: <number> }
{ $trunc: <number> }
```

### String Operators

```javascript
{ $concat: ["$firstName", " ", "$lastName"] }
{ $substr: ["$name", 0, 3] }
{ $toLower: "$name" }
{ $toUpper: "$name" }
{ $split: ["$tags", ","] }
{ $strcasecmp: ["$a", "$b"] }
{ $indexOfBytes: ["$name", "abc"] }
{ $indexOfCP: ["$name", "abc"] }
{ $strLenBytes: "$name" }
{ $strLenCP: "$name" }
```

### Date Operators

```javascript
{ $year: "$date" }
{ $month: "$date" }
{ $dayOfMonth: "$date" }
{ $hour: "$date" }
{ $minute: "$date" }
{ $second: "$date" }
{ $millisecond: "$date" }
{ $dayOfWeek: "$date" }
{ $dayOfYear: "$date" }
{ $week: "$date" }
{ $dateToString: { format: "%Y-%m-%d", date: "$date" } }
{ $dateFromString: { dateString: "$dateStr" } }
```

### Conditional Operators

```javascript
// If-then-else
{
  $cond: {
    if: { $gte: ["$score", 60] },
    then: "pass",
    else: "fail"
  }
}

// Switch/case
{
  $switch: {
    branches: [
      { case: { $eq: ["$status", "A"] }, then: "Active" },
      { case: { $eq: ["$status", "P"] }, then: "Pending" }
    ],
    default: "Unknown"
  }
}

// Coalesce (first non-null)
{ $ifNull: ["$field", "default-value"] }
```

### Array Operators

```javascript
{ $size: "$array" }
{ $isArray: "$field" }
{ $arrayElemAt: ["$array", 0] }
{ $concatArrays: [["$a"], ["$b"]] }
{ $slice: ["$array", 0, 5] }
{ $filter: {
    input: "$items",
    as: "item",
    cond: { $gt: ["$$item.price", 10] }
}}
{ $map: {
    input: "$items",
    as: "item",
    in: { price: { $multiply: ["$$item.price", 1.1] } }
}}
{ $reduce: {
    input: "$scores",
    initialValue: 0,
    in: { $add: ["$$value", "$$this"] }
}}
```

### Set Operators

```javascript
{ $setEquals: [["$a", "$b"], ["$b", "$a"]] }
{ $setIntersection: [["$a", "$b"], ["$b", "$c"]] }
{ $setUnion: [["$a", "$b"], ["$b", "$c"]] }
{ $setDifference: [["$a", "$b"], ["$b", "$c"]] }
{ $setIsSubset: [["$a", "$b"], [["$a", "$b", "$c"]] }
{ $anyElementTrue: [[true, false]] }
{ $allElementsTrue: [[true, false]] }
```

## Common Aggregation Patterns

### Funnel Analysis

Track user progression through steps:

```javascript
db.users.aggregate([
  { $match: { createdAt: { $gte: ISODate("2024-01-01") } } },
  { $facet: {
    visited: [
      { $match: { visited: true } },
      { $count: "visited" }
    ],
    signedUp: [
      { $match: { signedUp: true } },
      { $count: "signedUp" }
    ],
    purchased: [
      { $match: { purchased: true } },
      { $count: "purchased" }
    ]
  }},
  { $project: {
    visited: { $arrayElemAt: ["$visited", 0] },
    signedUp: { $arrayElemAt: ["$signedUp", 0] },
    purchased: { $arrayElemAt: ["$purchased", 0] }
  }}
])
```

### Time Series Analysis

Group by date intervals:

```javascript
db.sales.aggregate([
  { $match: { date: { $gte: ISODate("2024-01-01") } } },
  { $group: {
    _id: {
      year: { $year: "$date" },
      month: { $month: "$date" },
      day: { $dayOfMonth: "$date" }
    },
    totalSales: { $sum: "$amount" },
    avgSale: { $avg: "$amount" },
    count: { $sum: 1 }
  }},
  { $sort: { "_id.year": 1, "_id.month": 1, "_id.day": 1 } }
])
```

### Bucket Aggregation

Group into predefined ranges:

```javascript
db.products.aggregate([
  { $bucket: {
    groupBy: "$price",
    boundaries: [0, 50, 100, 200, 500],
    default: "Other",
    output: {
      count: { $sum: 1 },
      products: { $push: "$name" }
    }
  }}
])
```

### Moving Average

Calculate moving average over time series:

```javascript
db.sales.aggregate([
  { $sort: { date: 1 } },
  { $group: {
    _id: { $dateToString: { format: "%Y-%m-%d", date: "$date" } },
    total: { $sum: "$amount" }
  }},
  { $setWindowFields: {
    sortBy: { _id: 1 },
    output: {
      movingAvg: {
        $avg: "$total",
        window: {
          documents: [-2, 0]  // 3-day moving average
        }
      }
    }
  }}
])
```

### Nested Array Aggregation

Flatten and aggregate nested arrays:

```javascript
db.orders.aggregate([
  { $unwind: "$items" },
  { $group: {
    _id: "$items.productId",
    totalSold: { $sum: "$items.quantity" },
    revenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] } }
  }},
  { $sort: { totalSold: -1 } }
])
```

## Performance Optimization

### Early Filtering

Place `$match` at pipeline start:

```javascript
// Bad - filter after expensive operations
db.sales.aggregate([
  { $group: { _id: "$product", total: { $sum: "$amount" } } },
  { $match: { total: { $gt: 1000 } } }
])

// Good - filter early
db.sales.aggregate([
  { $match: { amount: { $gt: 100 } } },
  { $group: { _id: "$product", total: { $sum: "$amount" } } }
])
```

### Limit Documents

Use `$limit` early when possible:

```javascript
db.sales.aggregate([
  { $sort: { date: -1 } },
  { $limit: 1000 },  // Only process recent 1000 documents
  { $group: { _id: "$category", total: { $sum: "$amount" } } }
])
```

### Use Covered Queries

Create indexes for `$match` stages:

```javascript
// Create compound index
db.sales.createIndex({ status: 1, date: 1 })

// Aggregation uses index
db.sales.aggregate([
  { $match: { status: "completed", date: { $gte: ISODate("2024-01-01") } } }
])
```

### Avoid Large Documents

Use `$project` to reduce document size:

```javascript
// Bad - processes entire document
db.users.aggregate([
  { $group: { _id: "$region", count: { $sum: 1 } } }
])

// Good - project only needed fields
db.users.aggregate([
  { $project: { region: 1 } },
  { $group: { _id: "$region", count: { $sum: 1 } } }
])
```

### Monitor with Explain

```javascript
db.sales.aggregate(pipeline, { explain: true })
```

## Additional Resources

### Reference Files

For detailed stage documentation and advanced patterns:
- **`references/stages.md`** - Complete stage reference
- **`references/expressions.md`** - Expression operators reference
- **`references/optimization.md`** - Advanced optimization techniques

### Example Files

Working examples in `examples/`:
- **`basic-pipelines.js`** - Common aggregation patterns
- **`advanced-analytics.js`** - Complex analytics examples
- **`lookup-patterns.js`** - Join operations

### Scripts

Utility scripts in `scripts/`:
- **`pipeline-builder.js`** - Build aggregation pipelines programmatically
- **`pipeline-explainer.js`** - Analyze pipeline performance
