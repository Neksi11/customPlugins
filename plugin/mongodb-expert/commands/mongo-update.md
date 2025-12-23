---
description: Update or delete MongoDB documents
argument-hint: [collection] [filter] [operation]
allowed-tools: Bash(mongo:*), Bash(mongosh:*)
---

Update or delete documents in the specified MongoDB collection.

Required arguments:
- $1: Collection name
- $2: Filter query (JSON format)
- $3: Update operation or --delete flag

Update operations:
- Set field: { $set: { status: "active" } }
- Unset field: { $unset: { temp: 1 } }
- Increment: { $inc: { count: 1 } }
- Multiply: { $mul: { price: 1.1 } }
- Push to array: { $push: { tags: "new-tag" } }
- Pull from array: { $pull: { tags: "old-tag" } }

Delete operation:
- Use --delete flag to remove matching documents

Before executing:
1. Show filter to be applied
2. Count documents that match filter
3. Preview the update operation
4. Ask for confirmation on bulk operations

Execute operation and:
1. Display number of documents matched
2. Display number of documents modified
3. Show execution time
4. Verify changes with sample query

Update options:
- --one: Update only first matching document (default for updateOne)
- --many: Update all matching documents (default for updateMany)
- --upsert: Create document if no match found
- --delete: Delete matching documents instead of updating

Error handling:
- Invalid filter syntax
- Invalid update operators
- Collection does not exist
- Permission errors

Examples:
/mongo-update users { status: "pending" } { $set: { status: "active" } }
/mongo-update products { _id: 123 } { $inc: { views: 1 } } --one
/mongo-update users { lastLogin: { $lt: "2023-01-01" } } --delete
/mongo-update orders { status: "paid" } { $set: { archived: true } } --many
