---
description: Create and run MongoDB migrations
argument-hint: [create|run|rollback|status] [migration-name]
allowed-tools: Bash(mongo:*), Bash(mongosh:*), Read, Write
---

Manage MongoDB database migrations and schema changes.

Required arguments:
- $1: Action (create, run, rollback, status)

Optional arguments:
- $2: Migration name (for create/run/rollback)

Actions:

1. create [migration-name]:
   Generate a new migration file with the specified name.
   Create file in migrations/ directory with template structure.
   Include forward() and backward() functions.

2. run [migration-name]:
   Execute the specified migration.
   Track migration in _migrations collection.
   Show progress and results.

3. rollback [migration-name]:
   Rollback the specified migration.
   Execute backward() function.
   Update _migrations collection.

4. status:
   Show migration status.
   List pending migrations.
   List completed migrations.

Migration template structure:
```javascript
/**
 * Migration: [description]
 * Version: [timestamp]
 */

function forward() {
  // Migration logic here
}

function backward() {
  // Rollback logic here
}
```

Use mongodb-migrations skill for:
- Migration best practices
- Schema transformation patterns
- Rollback strategies
- Production deployment guidelines

Safety checks:
1. Backup database before running migrations
2. Validate migration syntax
3. Dry-run mode for preview
4. Transaction support (MongoDB 4.0+)

Error handling:
- Invalid migration file format
- Migration execution failures
- Rollback failures
- Database connection issues

Examples:
/mongo-migrate create add_status_field
/mongo-migrate run 001_add_status_field
/mongo-migrate rollback 001_add_status_field
/mongo-migrate status
