# MongoDB Expert Plugin

A comprehensive MongoDB integration plugin for Claude Code with query operations, aggregations, migrations, and VS Code extension support.

## Features

- **Query Operations**: Execute find, insert, update, and delete operations
- **Aggregation Pipelines**: Build and run complex aggregations
- **Schema Management**: View collections, indexes, and statistics
- **Migration Support**: Create and run database migrations
- **Query Optimization**: Analyze and optimize query performance
- **VS Code Extension**: Syntax highlighting, autocomplete, and results panel
- **MCP Integration**: Direct MongoDB server integration

## Installation

### Option 1: Local Plugin Directory

1. Copy the `mongodb-expert` folder to your project's `.claude-plugins/` directory
2. Restart Claude Code

### Option 2: Global Plugin

1. Copy to `~/.claude/plugins/mongodb-expert/`
2. Restart Claude Code

### Option 3: Marketplace

```bash
# Install from marketplace (when available)
claude-code plugin install mongodb-expert
```

## Prerequisites

- MongoDB connection (local or remote)
- Python 3.8+ (for MCP server)
- pymongo library: `pip install pymongo`

## Configuration

### Connection Settings

Create `.claude/mongodb-expert.local.md` in your project:

```yaml
---
connectionUri: mongodb://localhost:27017
defaultDatabase: myapp
timeout: 30000
debugMode: false
---
```

### Environment Variables

```bash
export MONGO_CONNECTION_URI="mongodb://localhost:27017"
export MONGO_DEFAULT_DATABASE="myapp"
export MONGO_TIMEOUT="30000"
export MONGO_DEBUG="false"
```

## Usage

### Commands

#### Connect to MongoDB
```
/mongo-connect mongodb://localhost:27017 myapp
```

#### Query Documents
```
/mongo-query users { status: "active" } { name: 1, email: 1, _id: 0 }
```

#### Insert Documents
```
/mongo-insert users { name: "John", email: "john@example.com" }
```

#### Update Documents
```
/mongo-update users { _id: 123 } { $set: { status: "active" } }
```

#### Run Aggregation
```
/mongo-aggregate sales [{ $match: { date: { $gte: "2024-01-01" } } }, { $group: { _id: "$category", total: { $sum: "$amount" } } }]
```

#### Create Migration
```
/mongo-migrate create add_status_field
```

#### Inspect Database
```
/mongo-inspect --collections
/mongo-inspect --indexes users
/mongo-inspect --stats products
```

### Skills

The plugin includes three skills that activate automatically:

1. **mongodb-query-patterns**: Activates when querying MongoDB
   - Query syntax and operators
   - Field projection and filtering
   - Performance optimization

2. **mongodb-aggregations**: Activates when building aggregations
   - Pipeline stages and operators
   - Complex data transformations
   - Optimization strategies

3. **mongodb-migrations**: Activates when managing schema changes
   - Migration patterns and best practices
   - Rollback strategies
   - Production deployment

### Agents

Two autonomous agents assist with MongoDB operations:

1. **query-optimizer** (blue)
   - Analyzes query performance
   - Suggests index improvements
   - Optimizes aggregation pipelines
   - Explains execution plans

2. **migration-validator** (yellow)
   - Validates migration scripts
   - Checks for data loss risks
   - Verifies rollback capability
   - Assesses production readiness

## VS Code Extension

The included VS Code extension provides:

### Features
- **Syntax Highlighting**: MongoDB query syntax
- **Code Snippets**: Common query patterns
- **Autocomplete**: Collection names and fields
- **Results Panel**: View query results in formatted panel

### Installation

```bash
cd vscode-extension
npm install
npm run compile
code --install-extension .
```

### VS Code Commands

| Command | Shortcut | Description |
|---------|----------|-------------|
| Run Query | Ctrl+Shift+Enter | Execute current query |
| Connect | - | Connect to MongoDB |
| Show Collections | - | List all collections |
| Explain Query | - | Show execution plan |

## Component Structure

```
mongodb-expert/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                 # Slash commands (7)
│   ├── mongo-connect.md
│   ├── mongo-query.md
│   ├── mongo-insert.md
│   ├── mongo-update.md
│   ├── mongo-aggregate.md
│   ├── mongo-migrate.md
│   └── mongo-inspect.md
├── agents/                   # Subagents (2)
│   ├── query-optimizer.md
│   └── migration-validator.md
├── skills/                   # Auto-activating skills (3)
│   ├── mongodb-query-patterns/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── examples/
│   │   └── scripts/
│   ├── mongodb-aggregations/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── examples/
│   │   └── scripts/
│   └── mongodb-migrations/
│       ├── SKILL.md
│       ├── references/
│       ├── examples/
│       └── scripts/
├── hooks/
│   └── hooks.json           # Event handlers
├── scripts/
│   └── mongodb-server.py    # MCP server
├── vscode-extension/
│   ├── package.json
│   ├── src/extension.ts
│   ├── syntax/
│   └── snippets/
├── .mcp.json                # MCP configuration
└── README.md
```

## MCP Server

The plugin includes a Python-based MCP server for MongoDB operations:

```python
# Scripts are executed via MCP integration
server.start()
```

Available MCP tools:
- `mongo_connect` - Connect to database
- `mongo_find` - Find documents
- `mongo_insert_one` - Insert document
- `mongo_update_one` - Update document
- `mongo_aggregate` - Run aggregation
- `mongo_list_collections` - List collections
- `mongo_get_stats` - Get statistics
- `mongo_list_indexes` - List indexes

## Advanced Usage

### Query Optimization

Ask the query-optimizer agent for help:

```
Can you optimize this query?
db.users.find({ age: { $gt: 18 }, status: "active" }).sort({ name: 1 })
```

### Migration Validation

Use the migration-validator agent before running migrations:

```
Please validate this migration script:
[script content]
```

### Aggregation Building

The mongodb-aggregations skill helps build pipelines:

```
Help me build an aggregation to group sales by category
```

## Troubleshooting

### Connection Issues

```
Error: Connection refused
```
- Verify MongoDB is running
- Check connection URI format
- Ensure network accessibility

### MCP Server Not Starting

```
Error: pymongo not installed
```
- Run: `pip install pymongo`

### Queries Not Executing

```
Error: Collection not found
```
- Verify collection name
- Check database context
- Use `/mongo-connect` first

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Created with Claude Code plugin-dev workflow.

## Version History

- **1.0.0** (2024-01-15)
  - Initial release
  - 7 commands for CRUD and operations
  - 3 skills for query patterns, aggregations, migrations
  - 2 agents for optimization and validation
  - MCP server integration
  - VS Code extension
