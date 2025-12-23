---
description: Connect to MongoDB database
argument-hint: [connection-uri] [database-name]
allowed-tools: Bash(mongo:*), Bash(mongosh:*)
---

Connect to MongoDB database using the provided connection URI and database name.

If $1 is provided:
  Use $1 as the connection URI
If $2 is provided:
  Use $2 as the database name
If no arguments provided:
  Check for connection settings in .claude/mongodb-expert.local.md
  Prompt user for connection details if not found

Connection options:
- Standard MongoDB URI: mongodb://host:port
- With authentication: mongodb://user:pass@host:port
- With SRV: mongodb+srv://cluster.example.com/
- Local instance: mongodb://localhost:27017

After connecting:
1. Test the connection with ping command
2. Show available databases
3. Display current database info
4. List collections in current database
5. Report connection status to user

Handle connection errors gracefully:
- Invalid URI format
- Authentication failures
- Network connectivity issues
- Database does not exist

Offer to save connection settings to .claude/mongodb-expert.local.md for future use.
