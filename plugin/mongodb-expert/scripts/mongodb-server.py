#!/usr/bin/env python3
"""
MongoDB MCP Server

A Model Context Protocol server that provides MongoDB database operations as tools.
Supports connection management, CRUD operations, aggregations, and schema inspection.
"""

import asyncio
import json
import os
import sys
from typing import Any, Optional
from datetime import datetime

try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
except ImportError:
    print("Error: pymongo not installed. Run: pip install pymongo", file=sys.stderr)
    sys.exit(1)


class MongoDBMCPServer:
    """MongoDB MCP Server implementation."""

    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connection_uri = os.getenv("MONGO_CONNECTION_URI", "mongodb://localhost:27017")
        self.default_database = os.getenv("MONGO_DEFAULT_DATABASE", "test")
        self.timeout = int(os.getenv("MONGO_TIMEOUT", "30000"))
        self.debug = os.getenv("MONGO_DEBUG", "false").lower() == "true"

    def log(self, message: str):
        """Log debug messages if debug mode is enabled."""
        if self.debug:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def connect(self) -> dict:
        """Connect to MongoDB."""
        try:
            if self.client is None:
                self.client = MongoClient(
                    self.connection_uri,
                    serverSelectionTimeoutMS=self.timeout
                )
                # Test connection
                self.client.admin.command('ping')
                self.db = self.client[self.default_database]
            return {
                "success": True,
                "message": f"Connected to MongoDB at {self.connection_uri}",
                "databases": self.client.list_database_names()
            }
        except ConnectionFailure as e:
            return {
                "success": False,
                "error": f"Connection failed: {str(e)}"
            }

    def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def find(self, collection: str, query: dict = None,
             projection: dict = None, limit: int = 100) -> dict:
        """Execute find query."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            query = query or {}
            projection = projection or {}

            cursor = coll.find(query, projection).limit(limit)
            results = list(cursor)

            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])

            return {
                "success": True,
                "count": len(results),
                "results": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def insert_one(self, collection: str, document: dict) -> dict:
        """Insert a single document."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            result = coll.insert_one(document)

            return {
                "success": True,
                "inserted_id": str(result.inserted_id),
                "message": "Document inserted successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def insert_many(self, collection: str, documents: list) -> dict:
        """Insert multiple documents."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            result = coll.insert_many(documents)

            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "inserted_ids": [str(id) for id in result.inserted_ids]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_one(self, collection: str, filter_query: dict,
                   update: dict, upsert: bool = False) -> dict:
        """Update a single document."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            result = coll.update_one(filter_query, update, upsert=upsert)

            return {
                "success": True,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": str(result.upserted_id) if result.upserted_id else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_many(self, collection: str, filter_query: dict,
                    update: dict) -> dict:
        """Update multiple documents."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            result = coll.update_many(filter_query, update)

            return {
                "success": True,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def delete_one(self, collection: str, filter_query: dict) -> dict:
        """Delete a single document."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            result = coll.delete_one(filter_query)

            return {
                "success": True,
                "deleted_count": result.deleted_count
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def delete_many(self, collection: str, filter_query: dict) -> dict:
        """Delete multiple documents."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            result = coll.delete_many(filter_query)

            return {
                "success": True,
                "deleted_count": result.deleted_count
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def aggregate(self, collection: str, pipeline: list) -> dict:
        """Execute aggregation pipeline."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            results = list(coll.aggregate(pipeline))

            # Convert ObjectId to string
            for doc in results:
                if '_id' in doc and isinstance(doc['_id'], dict):
                    doc['_id'] = {k: str(v) if k == '_id' else v for k, v in doc['_id'].items()}
                elif '_id' in doc:
                    doc['_id'] = str(doc['_id'])

            return {
                "success": True,
                "count": len(results),
                "results": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def count(self, collection: str, query: dict = None) -> dict:
        """Count documents."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            query = query or {}
            count = coll.count_documents(query)

            return {
                "success": True,
                "count": count
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_collections(self) -> dict:
        """List all collections."""
        try:
            if not self.db:
                self.connect()

            collections = self.db.list_collection_names()
            return {
                "success": True,
                "collections": collections
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_collection_stats(self, collection: str) -> dict:
        """Get collection statistics."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            stats = self.db.command("collstats", collection)

            return {
                "success": True,
                "stats": {
                    "count": stats.get("count", 0),
                    "size": stats.get("size", 0),
                    "avgObjSize": stats.get("avgObjSize", 0),
                    "storageSize": stats.get("storageSize", 0),
                    "totalIndexSize": stats.get("totalIndexSize", 0),
                    "nindexes": stats.get("nindexes", 0)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_indexes(self, collection: str) -> dict:
        """List indexes for a collection."""
        try:
            if not self.db:
                self.connect()

            coll = self.db[collection]
            indexes = coll.list_indexes()
            index_list = []
            for idx in indexes:
                index_list.append({
                    "name": idx.get("name"),
                    "keys": idx.get("key", {}),
                    "unique": idx.get("unique", False),
                    "sparse": idx.get("sparse", False)
                })

            return {
                "success": True,
                "indexes": index_list
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# JSON-RPC protocol handlers
def handle_request(request: dict, server: MongoDBMCPServer) -> dict:
    """Handle incoming JSON-RPC request."""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "mongodb-expert",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "mongo_connect",
                        "description": "Connect to MongoDB database",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "uri": {"type": "string", "description": "MongoDB connection URI"},
                                "database": {"type": "string", "description": "Database name"}
                            }
                        }
                    },
                    {
                        "name": "mongo_find",
                        "description": "Find documents in collection",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "collection": {"type": "string"},
                                "query": {"type": "object"},
                                "projection": {"type": "object"},
                                "limit": {"type": "integer", "default": 100}
                            },
                            "required": ["collection"]
                        }
                    },
                    {
                        "name": "mongo_insert_one",
                        "description": "Insert a single document",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "collection": {"type": "string"},
                                "document": {"type": "object"}
                            },
                            "required": ["collection", "document"]
                        }
                    },
                    {
                        "name": "mongo_update_one",
                        "description": "Update a single document",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "collection": {"type": "string"},
                                "filter": {"type": "object"},
                                "update": {"type": "object"},
                                "upsert": {"type": "boolean", "default": False}
                            },
                            "required": ["collection", "filter", "update"]
                        }
                    },
                    {
                        "name": "mongo_aggregate",
                        "description": "Execute aggregation pipeline",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "collection": {"type": "string"},
                                "pipeline": {"type": "array", "items": {"type": "object"}}
                            },
                            "required": ["collection", "pipeline"]
                        }
                    },
                    {
                        "name": "mongo_list_collections",
                        "description": "List all collections",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "mongo_get_stats",
                        "description": "Get collection statistics",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "collection": {"type": "string"}
                            },
                            "required": ["collection"]
                        }
                    },
                    {
                        "name": "mongo_list_indexes",
                        "description": "List indexes for collection",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "collection": {"type": "string"}
                            },
                            "required": ["collection"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        result = {}
        if tool_name == "mongo_connect":
            uri = arguments.get("uri", server.connection_uri)
            database = arguments.get("database", server.default_database)
            server.connection_uri = uri
            server.default_database = database
            server.db = None
            server.client = None
            result = server.connect()

        elif tool_name == "mongo_find":
            result = server.find(
                arguments["collection"],
                arguments.get("query"),
                arguments.get("projection"),
                arguments.get("limit", 100)
            )

        elif tool_name == "mongo_insert_one":
            result = server.insert_one(
                arguments["collection"],
                arguments["document"]
            )

        elif tool_name == "mongo_update_one":
            result = server.update_one(
                arguments["collection"],
                arguments["filter"],
                arguments["update"],
                arguments.get("upsert", False)
            )

        elif tool_name == "mongo_aggregate":
            result = server.aggregate(
                arguments["collection"],
                arguments["pipeline"]
            )

        elif tool_name == "mongo_list_collections":
            result = server.list_collections()

        elif tool_name == "mongo_get_stats":
            result = server.get_collection_stats(arguments["collection"])

        elif tool_name == "mongo_list_indexes":
            result = server.list_indexes(arguments["collection"])

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, default=str)
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }


def main():
    """Main MCP server loop."""
    server = MongoDBMCPServer()

    # Send initialization response
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "mongodb-expert",
                "version": "1.0.0"
            },
            "capabilities": {
                "tools": {}
            }
        }
    }), flush=True)

    # Process stdin/stdout
    while True:
        try:
            line = input()
            if not line:
                continue

            request = json.loads(line)
            response = handle_request(request, server)
            print(json.dumps(response), flush=True)

        except EOFError:
            break
        except json.JSONDecodeError:
            continue
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }), flush=True)


if __name__ == "__main__":
    main()
