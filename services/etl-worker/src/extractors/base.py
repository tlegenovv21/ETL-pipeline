from abc import ABC, abstractmethod
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseExtractor(ABC):
    """
    Abstract Base Class for all extractors.
    Enforces a standard structure.
    """
    
    def __init__(self, source_name):
        self.source_name = source_name

    @abstractmethod
    def extract(self, **kwargs):
        """
        Main method to fetch data. Must be implemented by subclasses.
        """
        pass

    def safe_request(self, func, *args, **kwargs):
        """
        Wrapper to handle errors and rate limits uniformly.
        """
        try:
            time.sleep(1)  # Rate limiting (1 second pause)
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {self.source_name}: {e}")
            return None