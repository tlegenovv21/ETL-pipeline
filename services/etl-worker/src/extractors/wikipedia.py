import requests
from .base import BaseExtractor, logger

class WikipediaExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("Wikipedia API")
        self.base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    def extract(self, topic):
        """
        Fetches the summary of a specific topic.
        """
        logger.info(f"Fetching Wikipedia article for: {topic}")
        
        url = f"{self.base_url}{topic}"
        
        # Using a lambda to pass the request to safe_request
        response = self.safe_request(requests.get, url)
        
        if response and response.status_code == 200:
            data = response.json()
            return {
                "source": "wikipedia",
                "topic": topic,
                "title": data.get("title"),
                "summary": data.get("extract"),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page")
            }
        else:
            logger.warning(f"Failed to fetch Wikipedia data for {topic}")
            return None