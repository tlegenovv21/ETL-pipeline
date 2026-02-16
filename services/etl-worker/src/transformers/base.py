from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, data):
        """
        Must be implemented by subclasses.
        """
        pass

    def unify_metadata(self, raw_id, source_type, data_type, content, metadata):
        """
        The Unified Metadata Schema for all data types.
        Every transformer must return data using this structure.
        """
        return {
            "file_id": str(raw_id) if raw_id else str(uuid.uuid4()),
            "source_type": source_type,      # e.g., 'wikipedia', 'unsplash', 'logs'
            "data_type": data_type,          # e.g., 'text', 'image', 'log'
            "processed_at": datetime.utcnow().isoformat(),
            "content": content,              # The cleaned text or the image URL
            "metadata": metadata             # Specific fields (hash, dimensions, language, etc.)
        }