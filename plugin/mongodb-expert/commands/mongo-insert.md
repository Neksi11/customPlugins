---
description: Insert documents into MongoDB collection
argument-hint: [collection] [document-json] | --file [filepath]
allowed-tools: Bash(mongo:*), Bash(mongosh:*), Read
---

Insert one or multiple documents into the specified MongoDB collection.

Required arguments:
- $1: Collection name

Optional arguments:
- $2: Document or array of documents (JSON format)
- --file: Path to JSON file containing documents

Document format:
- Single: { name: "John", email: "john@example.com" }
- Multiple: [{ name: "John" }, { name: "Jane" }]

If using --file flag:
1. Read the JSON file at $2
2. Validate JSON structure
3. Insert documents into collection

Before inserting:
1. Validate collection exists (or create if not)
2. Validate document structure
3. Check for required _id field conflicts
4. Show preview of documents to be inserted

After inserting:
1. Display inserted document IDs
2. Show count of inserted documents
3. Report any validation errors or duplicates
4. Verify insertion by querying inserted documents

Error handling:
- Invalid JSON format
- Duplicate _id errors
- Collection creation failures
- Validation constraint violations

Examples:
/mongo-insert users { name: "John", age: 30 }
/mongo-insert products --file ./data/products.json
/mongo-insert logs [{ event: "login" }, { event: "logout" }]
