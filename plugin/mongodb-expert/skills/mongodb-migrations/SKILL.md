---
name: mongodb-migrations
description: This skill should be used when the user asks to "migrate MongoDB", "MongoDB schema migration", "change MongoDB schema", "MongoDB migration script", "database migration", "rollback migration", or asks about MongoDB schema design, data transformation, or version control for database changes. Provides comprehensive MongoDB migration guidance.
version: 1.0.0
---

# MongoDB Migrations and Schema Management

## Purpose

This skill provides comprehensive guidance for managing MongoDB schema changes, data migrations, and database versioning. Cover migration strategies, rollback procedures, and best practices for evolving MongoDB schemas safely.

## When to Use

Activate this skill when working with MongoDB migrations including:
- Planning schema changes
- Writing migration scripts
- Data transformation and reshaping
- Index creation and management
- Rollback strategies
- Production database updates
- Schema validation and testing

## MongoDB Schema Philosophy

MongoDB's flexible schema requires intentional migration practices:

**Key Principles:**
1. **Schemaless != Chaotic**: Maintain schema documentation
2. **Graceful degradation**: Support old and new formats during transitions
3. **Backward compatibility**: Ensure old code works with new data
4. **Incremental migrations**: Small, reversible changes
5. **Test thoroughly**: Validate migrations on production-like data

## Migration Strategy Patterns

### 1. Expand and Contract Pattern

Add new fields before removing old ones:

```javascript
// Step 1: Add new field (expand)
db.users.updateMany(
  { },  // All documents
  { $set: { fullName: { $concat: ["$firstName", " ", "$lastName"] } } }
)

// Step 2: Deploy code using new field

// Step 3: Remove old field (contract)
db.users.updateMany(
  { fullName: { $exists: true } },
  { $unset: { firstName: 1, lastName: 1 } }
)
```

### 2. Default Values Pattern

Set defaults for existing documents:

```javascript
db.products.updateMany(
  { status: { $exists: false } },
  { $set: { status: "active", createdAt: new Date() } }
)
```

### 3. Data Type Conversion Pattern

Convert field types safely:

```javascript
// String to number
db.products.find({ price: { $type: "string" } }).forEach(doc => {
  db.products.updateOne(
    { _id: doc._id },
    { $set: { price: parseFloat(doc.price) } }
  )
})

// With error handling
db.products.find({ quantity: { $type: "string" } }).forEach(doc => {
  const num = parseInt(doc.quantity, 10)
  if (!isNaN(num)) {
    db.products.updateOne(
      { _id: doc._id },
      { $set: { quantity: num } }
    )
  } else {
    print(`Warning: Invalid quantity for document ${doc._id}`)
  }
})
```

### 4. Array to Nested Documents Pattern

Restructure arrays to nested documents:

```javascript
// Before: { tags: ["tag1", "tag2", "tag3"] }
// After: { tags: [{ name: "tag1", count: 0 }, ...] }

db.posts.find({ tags: { $type: "array", $not: { $type: "object" } } }).forEach(doc => {
  const newTags = doc.tags.map(tag => ({ name: tag, count: 0 }))
  db.posts.updateOne(
    { _id: doc._id },
    { $set: { tags: newTags } }
  )
})
```

## Common Migration Tasks

### Add New Field with Default

```javascript
db.collection.updateMany(
  { newField: { $exists: false } },
  { $set: { newField: "default-value" } }
)
```

### Rename Field

```javascript
db.collection.updateMany(
  { oldName: { $exists: true } },
  { $rename: { oldName: "newName" } }
)
```

### Change Field Type

```javascript
// Using aggregation (MongoDB 4.2+)
db.collection.updateMany(
  { },
  [
    { $set: {
      numericField: { $toDecimal: "$stringField" }
    }},
    { $unset: "stringField" }
  ]
)
```

### Extract Nested Field

```javascript
// Pull nested field to top level
db.users.updateMany(
  { "address.city": { $exists: true } },
  { $set: { city: "$address.city" } }
)
```

### Merge Collections

```javascript
// Merge source collection into target
db.source.find().forEach(doc => {
  doc.migratedAt = new Date()
  db.target.insertOne(doc)
})

// Verify migration
const sourceCount = db.source.countDocuments()
const targetCount = db.target.countDocuments({ migratedAt: { $exists: true } })
print(`Source: ${sourceCount}, Target: ${targetCount}`)
```

### Split Collection

```javascript
// Split orders into active and archived
db.orders.find({ status: "archived" }).forEach(doc => {
  db.orders_archived.insertOne(doc)
  db.orders.deleteOne({ _id: doc._id })
})
```

## Index Migrations

### Create Index Non-Blocking

```javascript
// For large collections, use background index creation
db.collection.createIndex(
  { field: 1 },
  { background: true }
)

// Or use rolling index creation (MongoDB 4.2+)
db.collection.createIndex(
  { field: 1 },
  { background: false }  // Faster, but blocks
)
```

### Drop Index

```javascript
// Drop specific index
db.collection.dropIndex("fieldName_1")

// Drop all indexes except _id
db.collection.dropIndexes()
```

### Modify Index

```javascript
// Indexes can't be modified - must recreate
db.collection.dropIndex("oldIndex")
db.collection.createIndex({ newField: 1 })
```

## Rollback Strategies

### Always Design Rollback First

```javascript
// Forward migration
function migrateForward() {
  db.users.updateMany(
    { status: { $exists: false } },
    { $set: { status: "active" } }
  )
}

// Rollback migration
function migrateBackward() {
  db.users.updateMany(
    { status: "active" },  // Only affect migrated documents
    { $unset: { status: 1 } }
  )
}
```

### Backup Before Migration

```javascript
// Create backup collection
db.collection_backup.insertMany(db.collection.find({}).toArray())

// Or use mongodump
// runCommand({
//   aggregate: "collection",
//   pipeline: [{ $out: "collection_backup" }],
//   cursor: {}
// })
```

### Transactional Rollback (MongoDB 4.0+)

```javascript
// Using transactions for multi-document migrations
const session = db.getMongo().startSession()
session.startTransaction()

try {
  db.users.updateMany(
    { },
    { $set: { migrated: true } },
    { session }
  )

  // Verify migration success
  const count = db.users.countDocuments({ migrated: true }, { session })

  if (count > 0) {
    session.commitTransaction()
    print("Migration committed")
  } else {
    session.abortTransaction()
    print("Migration aborted")
  }
} catch (error) {
  session.abortTransaction()
  print("Migration failed:", error)
} finally {
  session.endSession()
}
```

## Migration Script Template

```javascript
/**
 * Migration: Add status field to users
 * Version: 001
 * Date: 2024-01-15
 */

function migrate() {
  print("Starting migration: 001_add_status_field")

  const total = db.users.countDocuments({ status: { $exists: false } })
  print(`Documents to migrate: ${total}`)

  const batchSize = 1000
  let migrated = 0

  // Process in batches
  while (migrated < total) {
    const result = db.users.updateMany(
      { status: { $exists: false } },
      { $set: { status: "active", migratedAt: new Date() } },
      { limit: batchSize }
    )

    migrated += result.modifiedCount
    print(`Migrated: ${migrated}/${total}`)

    if (result.modifiedCount === 0) break
  }

  print("Migration complete: 001_add_status_field")
}

function rollback() {
  print("Rolling back migration: 001_add_status_field")

  const result = db.users.updateMany(
    { migratedAt: { $exists: true } },
    { $unset: { status: 1, migratedAt: 1 } }
  )

  print(`Rollback complete. Affected: ${result.modifiedCount}`)
}

// Run migration
migrate()
```

## Testing Migrations

### Dry Run Mode

```javascript
function dryRun() {
  print("DRY RUN - No changes will be made")

  const cursor = db.users.find({ status: { $exists: false } })
  const count = cursor.count()

  print(`Documents that would be affected: ${count}`)

  // Sample first few documents
  cursor.limit(5).forEach(doc => {
    print("Would update:", doc._id)
  })
}

dryRun()
```

### Validate Before Commit

```javascript
function validate() {
  const issues = []

  // Check for null values
  const nullCount = db.users.countDocuments({ status: null })
  if (nullCount > 0) {
    issues.push(`Found ${nullCount} documents with null status`)
  }

  // Check for invalid values
  const invalidCount = db.users.countDocuments({
    status: { $nin: ["active", "inactive", "pending"] }
  })
  if (invalidCount > 0) {
    issues.push(`Found ${invalidCount} documents with invalid status`)
  }

  if (issues.length > 0) {
    print("VALIDATION FAILED:")
    issues.forEach(issue => print("  -", issue))
    return false
  }

  print("VALIDATION PASSED")
  return true
}
```

## Production Deployment

### Pre-Migration Checklist

- [ ] Migration tested on staging environment
- [ ] Rollback procedure tested
- [ ] Database backup created
- [ ] Application compatible with both old and new schema
- [ ] Monitoring alerts configured
- [ ] Migration window approved
- [ ] Rollback plan communicated

### Deployment Steps

```javascript
// 1. Create backup
// mongodump --db=production --out=/backup/$(date +%Y%m%d)

// 2. Verify backup integrity
// mongorestore --db=test --drop /backup/20240115

// 3. Run dry-run
dryRun()

// 4. Validate pre-migration state
validate()

// 5. Execute migration
migrate()

// 6. Validate post-migration state
validate()

// 7. Monitor application logs
```

### Monitoring During Migration

```javascript
// Track migration progress
db.migrations.insertOne({
  version: "001",
  name: "add_status_field",
  startedAt: new Date(),
  status: "in_progress"
})

// Update on completion
db.migrations.updateOne(
  { version: "001" },
  {
    $set: {
      status: "completed",
      completedAt: new Date(),
      documentsMigrated: <count>
    }
  }
)
```

## Schema Versioning

### Track Schema Versions

```javascript
db.schema_versions.insertOne({
  collection: "users",
  version: 2,
  changes: [
    "Added status field",
    "Added migratedAt timestamp"
  ],
  migratedAt: new Date(),
  migrationScript: "001_add_status_field.js"
})
```

### Version Check Middleware

```javascript
// Application code to check schema version
function checkSchemaVersion(collection, requiredVersion) {
  const schema = db.schema_versions.findOne({ collection })
  if (!schema || schema.version < requiredVersion) {
    throw new Error(
      `Schema version mismatch. Expected ${requiredVersion}, got ${schema?.version}`
    )
  }
}
```

## Additional Resources

### Reference Files

For detailed migration patterns and best practices:
- **`references/patterns.md`** - Advanced migration patterns
- **`references/rollback.md`** - Rollback strategies
- **`references/production.md`** - Production deployment guide

### Example Files

Working examples in `examples/`:
- **`add-field.js`** - Add new field migration
- **`change-type.js`** - Type conversion migration
- **`refactor-schema.js`** - Schema refactoring example
- **`index-migration.js`** - Index management

### Scripts

Utility scripts in `scripts/`:
- **`migration-runner.js`** - Execute migrations in order
- **`migration-validator.js`** - Validate migration safety
- **`rollback-generator.js`** - Generate rollback scripts
