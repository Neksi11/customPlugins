# MongoDB Geospatial Query Patterns

Complete guide to geospatial queries and operations in MongoDB.

## Geospatial Data Models

MongoDB supports two types of geospatial data:

### 1. Legacy Coordinate Pairs

```javascript
// Legacy format: [longitude, latitude]
{
  name: "New York",
  loc: [ -73.935242, 40.730610 ]
}

// Create 2d index
db.places.createIndex({ loc: "2d" })
```

### 2. GeoJSON Objects (Recommended)

```javascript
// GeoJSON Point
{
  name: "New York",
  location: {
    type: "Point",
    coordinates: [ -73.935242, 40.730610 ]  // [longitude, latitude]
  }
}

// Create 2dsphere index
db.places.createIndex({ location: "2dsphere" })
```

## GeoJSON Geometry Types

### Point

```javascript
{
  "type": "Point",
  "coordinates": [ -73.935242, 40.730610 ]
}
```

### LineString

```javascript
{
  "type": "LineString",
  "coordinates": [
    [ -73.935242, 40.730610 ],
    [ -73.945242, 40.740610 ],
    [ -73.955242, 40.750610 ]
  ]
}
```

### Polygon

```javascript
{
  "type": "Polygon",
  "coordinates": [[
    [ -73.935242, 40.730610 ],
    [ -73.945242, 40.730610 ],
    [ -73.945242, 40.740610 ],
    [ -73.935242, 40.740610 ],
    [ -73.935242, 40.730610 ]  // Close the loop
  ]]
}
```

### MultiPoint

```javascript
{
  "type": "MultiPoint",
  "coordinates": [
    [ -73.935242, 40.730610 ],
    [ -73.945242, 40.740610 ]
  ]
}
```

### MultiPolygon

```javascript
{
  "type": "MultiPolygon",
  "coordinates": [[
    // Polygon 1
    [[...]]
  ], [
    // Polygon 2
    [[...]]
  ]]
}
```

## Geospatial Operators

### $near

Find points near a location (requires geospatial index):

```javascript
// Find places near New York, sorted by distance
db.places.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [ -73.935242, 40.730610 ]
      },
      $maxDistance: 5000,  // meters
      $minDistance: 100    // meters
    }
  }
})
```

### $geoWithin

Find points within a geometry:

```javascript
// Points within a circle
db.places.find({
  location: {
    $geoWithin: {
      $centerSphere: [
        [ -73.935242, 40.730610 ],  // center
        5 / 3963.2                  // radius in radians (5 miles / Earth radius)
      ]
    }
  }
})

// Points within a polygon
db.places.find({
  location: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [ -73.935242, 40.730610 ],
          [ -73.945242, 40.730610 ],
          [ -73.945242, 40.740610 ],
          [ -73.935242, 40.740610 ],
          [ -73.935242, 40.730610 ]
        ]]
      }
    }
  }
})

// Points within a box
db.places.find({
  location: {
    $geoWithin: {
      $box: [
        [ -73.95, 40.73 ],  // bottom-left
        [ -73.93, 40.75 ]   // top-right
      ]
    }
  }
})
```

### $geoIntersects

Find locations that intersect with a geometry:

```javascript
// Find places intersecting a polygon
db.places.find({
  location: {
    $geoIntersects: {
      $geometry: {
        type: "Polygon",
        coordinates: [[
          [ -73.935242, 40.730610 ],
          [ -73.945242, 40.730610 ],
          [ -73.945242, 40.740610 ],
          [ -73.935242, 40.740610 ],
          [ -73.935242, 40.730610 ]
        ]]
      }
    }
  }
})
```

### $nearSphere

Same as $near but uses spherical geometry:

```javascript
db.places.find({
  location: {
    $nearSphere: {
      $geometry: {
        type: "Point",
        coordinates: [ -73.935242, 40.730610 ]
      },
      $maxDistance: 1000  // meters
    }
  }
})
```

## Distance Calculations

### Using $geoNear Aggregation

```javascript
db.places.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [ -73.935242, 40.730610 ]
      },
      distanceField: "distance",      // Field to store distance
      maxDistance: 5000,              // Maximum distance in meters
      spherical: true,                // Use spherical geometry
      distanceMultiplier: 0.000621371 // Convert meters to miles
    }
  },
  { $limit: 10 }
])
```

### Using $project with Distance

```javascript
db.places.aggregate([
  {
    $geoNear: {
      near: { type: "Point", coordinates: [ -73.935242, 40.730610 ] },
      distanceField: "distance",
      spherical: true
    }
  },
  {
    $project: {
      name: 1,
      distance: { $round: ["$distance", 2] },  // Round to 2 decimals
      distanceKm: { $divide: ["$distance", 1000] }
    }
  }
])
```

## Common Patterns

### Find Nearby and Sort by Distance

```javascript
db.places.aggregate([
  {
    $geoNear: {
      near: { type: "Point", coordinates: [ -73.935242, 40.730610 ] },
      distanceField: "distance",
      spherical: true
    }
  },
  { $limit: 20 },
  {
    $project: {
      name: 1,
      type: 1,
      distance: 1,
      distanceKm: { $round: [{ $divide: ["$distance", 1000] }, 2] }
    }
  }
])
```

### Find Points Within Radius

```javascript
const center = [ -73.935242, 40.730610 ]
const radiusKm = 5
const radiusRadians = radiusKm / 6378.1  // Earth's radius in km

db.places.find({
  location: {
    $geoWithin: {
      $centerSphere: [ center, radiusRadians ]
    }
  }
})
```

### Find Points in Bounding Box

```javascript
// Southwest corner to Northeast corner
db.places.find({
  location: {
    $geoWithin: {
      $box: [
        [ -73.95, 40.73 ],  // Southwest
        [ -73.93, 40.75 ]   // Northeast
      ]
    }
  }
})
```

### Multi-Location Search

Search multiple points and return closest for each:

```javascript
const locations = [
  { type: "Point", coordinates: [ -73.935242, 40.730610 ] },  // NY
  { type: "Point", coordinates: [ -118.243683, 34.052235 ] }  // LA
]

// For each location, find nearby places
locations.forEach(loc => {
  const nearby = db.places.find({
    location: {
      $near: {
        $geometry: loc,
        $maxDistance: 5000
      }
    }
  }).limit(5)
})
```

## Performance Tips

1. **Always create 2dsphere index** for GeoJSON queries
2. **Use $geoNear aggregation** when you need distance calculations
3. **Use $maxDistance** to limit result set size
4. **Consider using $geometry** instead of legacy coordinate pairs
5. **Use spherical: true** for accurate Earth distance calculations

## Unit Conversions

### Distance Conversions

```javascript
// Miles to radians
const milesToRadians = (miles) => miles / 3963.2

// Kilometers to radians
const kmToRadians = (km) => km / 6378.1

// Meters to radians
const metersToRadians = (meters) => meters / 6378100

// Meters to miles
const metersToMiles = (meters) => meters * 0.000621371
```

### Examples

```javascript
// 5 miles radius
$centerSphere: [[ -73.935242, 40.730610 ], 5 / 3963.2]

// 10 km radius
$centerSphere: [[ -73.935242, 40.730610 ], 10 / 6378.1]

// 5000 meters radius
$maxDistance: 5000  // meters
```

## Index Configuration

```javascript
// Basic 2dsphere index
db.places.createIndex({ location: "2dsphere" })

// 2dsphere index with bucket size
db.places.createIndex({ location: "2dsphere" }, { bucketSize: 1 })

// Compound index with geospatial field
db.places.createIndex({ location: "2dsphere", category: 1 })

// Sparse geospatial index (only index documents with location field)
db.places.createIndex({ location: "2dsphere" }, { sparse: true })
```

## Error Handling

```javascript
// Check if point is valid
function isValidPoint(geojson) {
  return geojson &&
         geojson.type === "Point" &&
         Array.isArray(geojson.coordinates) &&
         geojson.coordinates.length === 2 &&
         Math.abs(geojson.coordinates[0]) <= 180 &&
         Math.abs(geojson.coordinates[1]) <= 90
}

// Validate before insert
if (isValidPoint(doc.location)) {
  db.places.insertOne(doc)
} else {
  print("Invalid GeoJSON Point")
}
```
