from apify_client import ApifyClient
from typing import List, Dict, Any
from .base_scraper import BaseScraper


class Yad2Scraper(BaseScraper):
    APIFY_YAD2_ACTOR = 'swerve/yad2-scraper'

    def __init__(self, api_token: str):
        super().__init__(api_token)
        self.source = 'Yad2'
        self.client = ApifyClient(api_token)

    def fetch_listings(self, location: str, min_price: int, max_price: int,
                      min_rooms: int, max_rooms: int) -> List[Dict[str, Any]]:
        """Fetch listings from Yad2 via Apify"""
        try:
            self.log_info(f"Fetching listings for {location} (₪{min_price}-{max_price}, {min_rooms}-{max_rooms} rooms)")

            input_data = {
                'searchType': 'rent',
                'city': location,
                'priceMin': min_price,
                'priceMax': max_price,
                'roomsMin': min_rooms,
                'roomsMax': max_rooms,
            }

            run = self.client.actor(self.APIFY_YAD2_ACTOR).call(run_input=input_data)
            raw_listings = self.client.dataset(run['defaultDatasetId']).list_items().items

            standardized = [self.standardize_listing(item) for item in raw_listings]
            valid_listings = [l for l in standardized if self.validate_listing(l)]

            self.log_info(f"Found {len(valid_listings)} valid listings (from {len(raw_listings)} total)")
            return valid_listings

        except Exception as e:
            self.log_error(f"Error fetching listings: {e}")
            return []

    def standardize_listing(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Yad2 data to standard format"""
        base = super().standardize_listing(raw_data)
        base.update({
            'title': raw_data.get('title') or raw_data.get('description', ''),
            'price': raw_data.get('price'),
            'rooms': raw_data.get('rooms'),
            'area': raw_data.get('area'),
            'location': raw_data.get('city', ''),
            'address': raw_data.get('address', ''),
            'url': raw_data.get('url') or raw_data.get('link', ''),
        })
        return base
