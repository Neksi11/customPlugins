---
description: Run MongoDB aggregation pipeline
argument-hint: [collection] [pipeline-json]
allowed-tools: Bash(mongo:*), Bash(mongosh:*)
---

Execute aggregation pipeline on the specified MongoDB collection.

Required arguments:
- $1: Collection name
- $2: Aggregation pipeline (JSON array format)

Pipeline format:
[{ $match: { status: "active" } }, { $group: { _id: "$category", total: { $sum: "$amount" } } }]

Common stages:
- $match: Filter documents
- $group: Aggregate documents
- $project: Reshape documents
- $sort: Sort results
- $limit: Restrict output
- $lookup: Join collections
- $unwind: Flatten arrays
- $count: Count documents

Before executing:
1. Validate pipeline syntax
2. Show pipeline stages in readable format
3. Estimate execution complexity
4. Check for indexes on $match stages

Execute aggregation and:
1. Display results in structured format
2. Show execution statistics
3. Report execution time
4. Suggest optimizations for slow pipelines

Use mongodb-aggregations skill for:
- Complex pipeline construction
- Stage selection and ordering
- Performance optimization
- Common aggregation patterns

Output options:
- Default: Pretty JSON results
- --explain: Show execution plan
- --stats: Show detailed statistics
- --count: Show result count only

Error handling:
- Invalid pipeline syntax
- Unknown aggregation stages
- Type mismatch in operators
- Memory limit exceeded

Examples:
/mongo-aggregate sales [{ $match: { date: { $gte: "2024-01-01" } } }, { $group: { _id: "$category", total: { $sum: "$amount" } } }]
/mongo-aggregate users [{ $group: { _id: "$region", count: { $sum: 1 } } }, { $sort: { count: -1 } }]
/mongo-aggregate orders [{ $lookup: { from: "customers", localField: "customerId", foreignField: "_id", as: "customer" } }] --explain
