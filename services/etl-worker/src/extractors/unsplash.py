import requests
import os
from .base import BaseExtractor, logger

class UnsplashExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("Unsplash API")
        self.access_key = os.getenv("UNSPLASH_ACCESS_KEY", "YOUR_KEY_HERE")
        self.base_url = "https://api.unsplash.com/search/photos"

    def extract(self, query, count=5):
        logger.info(f"Searching Unsplash for: {query}")
        params = {"query": query, "per_page": count, "client_id": self.access_key}
        response = self.safe_request(requests.get, self.base_url, params=params)
        
        if response and response.status_code == 200:
            results = response.json().get("results", [])
            images = []
            for img in results:
                images.append({
                    "source": "unsplash",
                    "id": img.get("id"),
                    "description": img.get("alt_description"),
                    "url": img.get("urls", {}).get("regular"),
                    "photographer": img.get("user", {}).get("name")
                })
            return images
        else:
            logger.warning("Failed to fetch Unsplash data")
            return []
        