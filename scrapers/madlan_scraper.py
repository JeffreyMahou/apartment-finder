import requests
from typing import List, Dict, Any
from .base_scraper import BaseScraper


class MadlanScraper(BaseScraper):
    APIFY_MADLAN_ACTOR = 'swerve/madlan-scraper'
    APIFY_API_URL = 'https://api.apify.com/v2'

    def __init__(self, api_token: str):
        super().__init__(api_token)
        self.source = 'Madlan'

    def fetch_listings(self, location: str, min_price: int, max_price: int,
                      min_rooms: int, max_rooms: int) -> List[Dict[str, Any]]:
        """Fetch listings from Madlan via Apify"""
        try:
            self.log_info(f"Fetching listings for {location} (₪{min_price}-{max_price}, {min_rooms}-{max_rooms} rooms)")

            input_data = {
                'dealType': 'rent',
                'cities': [location],
                'priceMin': min_price,
                'priceMax': max_price,
                'roomsMin': min_rooms,
                'roomsMax': max_rooms,
            }

            url = f'{self.APIFY_API_URL}/acts/{self.APIFY_MADLAN_ACTOR}/run-sync-get-dataset-items'
            params = {
                'token': self.api_token
            }

            response = requests.post(url, json=input_data, params=params, timeout=60)
            response.raise_for_status()

            raw_listings = response.json()
            standardized = [self.standardize_listing(item) for item in raw_listings]
            valid_listings = [l for l in standardized if self.validate_listing(l)]

            self.log_info(f"Found {len(valid_listings)} valid listings (from {len(raw_listings)} total)")
            return valid_listings

        except requests.exceptions.RequestException as e:
            self.log_error(f"API request failed: {e}")
            return []
        except Exception as e:
            self.log_error(f"Error fetching listings: {e}")
            return []

    def standardize_listing(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Madlan data to standard format"""
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
