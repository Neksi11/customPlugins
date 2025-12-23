---
description: Query MongoDB with find operations
argument-hint: [collection] [query] [projection]
allowed-tools: Bash(mongo:*), Bash(mongosh:*)
---

Execute MongoDB find query on the specified collection.

Required arguments:
- $1: Collection name to query

Optional arguments:
- $2: Query filter (JSON format)
- $3: Field projection (JSON format)

Query format:
- Simple: { status: "active" }
- With operators: { age: { $gt: 18 } }
- Multiple fields: { status: "active", age: { $gte: 18 } }

Projection format:
- Include: { name: 1, email: 1 }
- Exclude: { password: 0, ssn: 0 }
- Mixed: { name: 1, _id: 0 }

Execute the query and:
1. Show execution statistics (docs scanned, time taken)
2. Display results in table format when possible
3. Limit output to 50 documents by default
4. Format JSON output for readability
5. Suggest indexes if query appears slow

Use mongodb-query-patterns skill for:
- Complex query construction
- Operator selection
- Performance optimization

Output modes:
- Default: Pretty JSON format
- --table: Table format (when applicable)
- --count: Return count only
- --explain: Show query execution plan

Examples:
/mongo-query users { status: "active" }
/mongo-query products { price: { $gt: 100 } } { name: 1, price: 1, _id: 0 }
/mongo-query orders {} {} --count
/mongo-query users { email: { $regex: "@gmail" } } --explain
