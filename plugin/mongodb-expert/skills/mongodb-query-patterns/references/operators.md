# MongoDB Query Operators Reference

Complete reference for MongoDB query operators organized by category.

## Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$eq` | Matches values equal to specified value | `{ field: { $eq: value } }` |
| `$gt` | Matches values greater than specified value | `{ field: { $gt: 100 } }` |
| `$gte` | Matches values greater than or equal to | `{ field: { $gte: 100 } }` |
| `$lt` | Matches values less than specified value | `{ field: { $lt: 100 } }` |
| `$lte` | Matches values less than or equal to | `{ field: { $lte: 100 } }` |
| `$ne` | Matches all values not equal to specified value | `{ field: { $ne: value } }` |
| `$in` | Matches any of the values in array | `{ field: { $in: [1, 2, 3] } }` |
| `$nin` | Matches none of the values in array | `{ field: { $nin: [1, 2, 3] } }` |

## Logical Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$and` | Joins clauses with logical AND | `{ $and: [{ qty: { $lt: 10 } }, { qty: { $gt: 5 } }] }` |
| `$or` | Joins clauses with logical OR | `{ $or: [{ price: 9.99 }, { price: { $exists: false } }] }` |
| `$not` | Inverts effect of query operator | `{ price: { $not: { $gt: 100 } } }` |
| `$nor` | Joins clauses with logical NOR | `{ $nor: [{ price: 1.99 }, { sale: true }] }` |

## Element Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$exists` | Matches documents with specified field | `{ field: { $exists: true } }` |
| `$type` | Matches documents where field is specified type | `{ field: { $type: "string" } }` |
|  |  | `{ field: { $type: ["string", "null"] } }` |

## Evaluation Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$mod` | Matches documents where field modulo divisor equals remainder | `{ qty: { $mod: [4, 0] } }` |
| `$regex` | Matches documents where field matches regex pattern | `{ name: { $regex: "^Acme" } }` |
| `$text` | Performs text search | `{ $text: { $search: "coffee" } }` |
| `$where` | Matches documents satisfying JavaScript expression | `{ $where: "this.credits == this.debits" }` |

**Note:** Use `$where` sparingly - it has performance and security implications.

## Array Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$all` | Matches arrays containing all elements | `{ tags: { $all: ["red", "blank"] } }` |
| `$elemMatch` | Matches if element in array matches all conditions | `{ results: { $elemMatch: { $gt: 80, $lt: 85 } } }` |
| `$size` | Matches arrays with specified size | `{ items: { $size: 3 } }` |

## Geospatial Operators

### Geometry Specifiers

| Operator | Description | Example |
|----------|-------------|---------|
| `$geoIntersects` | Matches geometries intersecting GeoJSON geometry | `{ loc: { $geoIntersects: { $geometry: ... } } }` |
| `$geoWithin` | Matches geometries within GeoJSON geometry | `{ loc: { $geoWithin: { $geometry: ... } } }` |
| `$near` | Returns geospatial objects near a point | `{ loc: { $near: { $geometry: ... } } }` |
| `$nearSphere` | Returns geospatial objects near sphere point | `{ loc: { $nearSphere: { $geometry: ... } } }` |

## Bitwise Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$bitsAllClear` | Matches where all bit positions are clear | `{ bitmask: { $bitsAllClear: [1, 5] } }` |
| `$bitsAllSet` | Matches where all bit positions are set | `{ bitmask: { $bitsAllSet: [1, 5] } }` |
| `$bitsAnyClear` | Matches where any bit position is clear | `{ bitmask: { $bitsAnyClear: [1, 5] } }` |
| `$bitsAnySet` | Matches where any bit position is set | `{ bitmask: { $bitsAnySet: [1, 5] } }` |

## Projection Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `$` | Projects first element matching query condition | `{ "students.$": 1 }` |
| `$elemMatch` | Projects first element matching $elemMatch condition | `{ students: { $elemMatch: { school: "A" } } }` |
| `$meta` | Projects text score document | `{ score: { $meta: "textScore" } }` |
| `$slice` | Limits portion of array projection | `{ attendees: { $slice: 3 } }` |

## Type Numbers

For `$type` operator, use these numbers:

| Type | Number | String Alias |
|------|--------|--------------|
| Double | 1 | "double" |
| String | 2 | "string" |
| Object | 3 | "object" |
| Array | 4 | "array" |
| Binary data | 5 | "binData" |
| ObjectId | 7 | "objectId" |
| Boolean | 8 | "bool" |
| Date | 9 | "date" |
| Null | 10 | "null" |
| Regular Expression | 11 | "regex" |
| JavaScript | 13 | "javascript" |
| 32-bit integer | 16 | "int" |
| Timestamp | 17 | "timestamp" |
| 64-bit integer | 18 | "long" |
| Decimal128 | 19 | "decimal" |
| MinKey | -1 | "minKey" |
| MaxKey | 127 | "maxKey" |

## Regex Options

Use with `$regex`:

| Option | Description |
|--------|-------------|
| `i` | Case insensitivity |
| `m` | Multiline matching |
| `x` | Extended mode (ignore whitespace) |
| `s` | Allow dot character (.) to match newline |
