// Basic MongoDB Query Examples
// Run in MongoDB shell or with mongosh

// ============================================
// 1. FIND ALL DOCUMENTS
// ============================================

// Find all documents in a collection
db.users.find()

// Find with pretty print
db.users.find().pretty()

// ============================================
// 2. EQUALITY FILTERS
// ============================================

// Single field equality
db.users.find({ status: "active" })

// Multiple field equality (implicit AND)
db.users.find({ status: "active", role: "admin" })

// ============================================
// 3. COMPARISON OPERATORS
// ============================================

// Greater than
db.products.find({ price: { $gt: 100 } })

// Less than or equal
db.products.find({ quantity: { $lte: 50 } })

// Not equal
db.users.find({ status: { $ne: "deleted" } })

// In array
db.users.find({ role: { $in: ["admin", "moderator"] } })

// ============================================
// 4. LOGICAL OPERATORS
// ============================================

// OR condition
db.users.find({
  $or: [
    { status: "active" },
    { status: "pending" }
  ]
})

// AND condition (explicit)
db.users.find({
  $and: [
    { age: { $gte: 18 } },
    { age: { $lt: 65 } }
  ]
})

// NOR condition
db.users.find({
  $nor: [
    { status: "deleted" },
    { status: "banned" }
  ]
})

// NOT condition
db.users.find({
  age: { $not: { $lt: 18 } }
})

// ============================================
// 5. FIELD PROJECTION
// ============================================

// Include specific fields
db.users.find(
  { status: "active" },
  { name: 1, email: 1 }
)

// Exclude specific fields
db.users.find(
  { status: "active" },
  { password: 0, ssn: 0 }
)

// Exclude _id
db.users.find(
  {},
  { _id: 0, name: 1, email: 1 }
)

// ============================================
// 6. ARRAY QUERIES
// ============================================

// Match array containing value
db.posts.find({ tags: "mongodb" })

// Match array containing multiple values
db.posts.find({ tags: { $all: ["mongodb", "nodejs"] } })

// Match exact array
db.posts.find({ tags: ["mongodb", "nodejs", "javascript"] })

// Match by array size
db.posts.find({ comments: { $size: 5 } })

// ============================================
// 7. NESTED DOCUMENT QUERIES
// ============================================

// Query nested field with dot notation
db.users.find({ "address.city": "New York" })

// Query nested array
db.users.find({ "orders.0.status": "shipped" })

// ============================================
// 8. NULL AND MISSING FIELDS
// ============================================

// Find documents where field is null or missing
db.users.find({ field: null })

// Find only where field exists but is null
db.users.find({ field: { $type: "null" } })

// Find where field exists (regardless of value)
db.users.find({ field: { $exists: true } })

// Find where field is missing
db.users.find({ field: { $exists: false } })

// ============================================
// 9. REGEX QUERIES
// ============================================

// Pattern matching
db.users.find({ name: { $regex: "^John" } })

// Case insensitive
db.users.find({ email: { $regex: "@gmail\\.com$", $options: "i" } })

// Contains text
db.users.find({ bio: { $regex: "developer", $options: "i" } })

// ============================================
// 10. SORTING AND LIMITING
// ============================================

// Sort ascending
db.users.find({}).sort({ name: 1 })

// Sort descending
db.users.find({}).sort({ created: -1 })

// Compound sort
db.users.find({}).sort({ lastName: 1, firstName: 1 })

// Limit results
db.users.find({}).limit(10)

// Skip and limit (pagination)
db.users.find({}).skip(20).limit(10)

// Combined: sort, skip, limit
db.users.find({})
  .sort({ created: -1 })
  .skip(0)
  .limit(20)

// ============================================
// 11. COUNTING
// ============================================

// Count all documents
db.users.countDocuments()

// Count with filter
db.users.countDocuments({ status: "active" })

// Estimated count (faster)
db.users.estimatedDocumentCount()

// ============================================
// 12. DISTINCT VALUES
// ============================================

// Get unique values
db.users.distinct("role")

// Get unique values with filter
db.users.distinct("department", { status: "active" })

// ============================================
// 13. EXPLAIN QUERY
// ============================================

// Check query plan
db.users.find({ email: "test@example.com" }).explain()

// Check execution stats
db.users.find({ email: "test@example.com" }).explain("executionStats")

// Check all execution plans
db.users.find({ email: "test@example.com" }).explain("allPlansExecution")

// ============================================
// 14. QUERY WITH COMMENTS
// ============================================

// Add comment for slow query log
db.users.find(
  { status: "active" },
  { _id: 0, name: 1 }
).comment("Get active user names for dashboard")
