---
description: Inspect MongoDB collections, indexes, and statistics
argument-hint: [--collections|--indexes|--stats|--schema] [collection-name]
allowed-tools: Bash(mongo:*), Bash(mongosh:*)
---

Inspect MongoDB database structure, collections, indexes, and statistics.

Required arguments:
- $1: Inspection type flag

Optional arguments:
- $2: Collection name (for collection-specific inspection)

Inspection types:

1. --collections [name]:
   List all collections in current database
   If collection name provided, show detailed collection info
   Display document count, size, and storage stats

2. --indexes [name]:
   Show indexes for specified collection
   If no collection provided, list all indexes across collections
   Display index details: keys, options, size, usage

3. --stats [name]:
   Show database or collection statistics
   Include: storage size, document count, index size, average document size
   Display data distribution info

4. --schema [name]:
   Analyze and display schema for collection
   Show field types, frequencies, and patterns
   Identify nested structures and arrays
   Detect schema variations

5. --all:
   Run all inspections
   Comprehensive database overview
   Structured report format

Display format:
- Table format for lists and stats
- JSON format for complex data
- Tree view for schema hierarchy

Analysis features:
1. Identify missing indexes
2. Detect unused indexes
3. Find large documents
4. Spot schema inconsistencies
5. Suggest optimizations

Output options:
- Default: Formatted tables
- --json: Raw JSON output
- --analyze: Include analysis and suggestions

Error handling:
- Collection does not exist
- Permission denied
- Database connection issues

Examples:
/mongo-inspect --collections
/mongo-inspect --indexes users
/mongo-inspect --stats products
/mongo-inspect --schema orders
/mongo-inspect --all
/mongo-inspect --indexes users --analyze
