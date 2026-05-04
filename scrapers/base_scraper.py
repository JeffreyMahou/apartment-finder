import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.source = self.__class__.__name__

    def standardize_listing(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert raw platform data to standard format"""
        return {
            'title': raw_data.get('title', ''),
            'price': raw_data.get('price'),
            'rooms': raw_data.get('rooms'),
            'area': raw_data.get('area'),
            'location': raw_data.get('location', ''),
            'address': raw_data.get('address', ''),
            'url': raw_data.get('url', ''),
            'source': self.source,
            'date_fetched': datetime.now().isoformat(),
            'raw_data': raw_data
        }

    @abstractmethod
    def fetch_listings(self, location: str, min_price: int, max_price: int,
                      min_rooms: int, max_rooms: int) -> List[Dict[str, Any]]:
        """Fetch listings from the platform"""
        pass

    def validate_listing(self, listing: Dict[str, Any]) -> bool:
        """Basic validation of listing data"""
        required_fields = ['price', 'url']
        return all(listing.get(field) for field in required_fields)

    def log_info(self, message: str):
        logger.info(f"[{self.source}] {message}")

    def log_error(self, message: str):
        logger.error(f"[{self.source}] {message}")
