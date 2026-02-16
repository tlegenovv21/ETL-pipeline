import os
from pymongo import MongoClient

class MongoLoader:
    def __init__(self):
        # Initialize MongoDB client
        uri = os.getenv("MONGO_URI", "mongodb://admin:supersecretkey@mongo:27017/")
        self.client = MongoClient(uri)
        self.db = self.client["metadata_db"]
        self.collection = self.db["metadata"]
        self._setup_validation()

    def _setup_validation(self):
        # Setup schema validation required by the project specifications
        validation_schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["file_id", "source_type", "processed_at"],
                "properties": {
                    "file_id": {"bsonType": "string"},
                    "source_type": {"bsonType": "string"},
                    "processed_at": {"bsonType": "string"}
                }
            }
        }
        try:
            # Try to apply validation to an existing collection
            self.db.command("collMod", "metadata", validator=validation_schema)
        except Exception:
            # If collection does not exist, create it with the validator
            self.db.create_collection("metadata", validator=validation_schema)

    def load_metadata(self, metadata):
        # Use upsert to prevent duplicates and ensure idempotency
        self.collection.update_one(
            {"file_id": metadata["file_id"]},
            {"$set": metadata},
            upsert=True
        )