import csv
import json
import logging
import sys
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

def safe_print(text):
    """Print text with graceful Unicode handling"""
    try:
        print(text, flush=True)
    except Exception:
        pass


class ListingFormatter:
    def __init__(self, output_dir: str = 'data'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_csv(self, listings: List[Dict[str, Any]], filename: str = None) -> str:
        """Save listings to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'listings_{timestamp}.csv'

        filepath = self.output_dir / filename

        if not listings:
            logger.warning("No listings to save")
            return str(filepath)

        # Define CSV columns (exclude raw_data)
        fieldnames = ['source', 'title', 'price', 'rooms', 'area', 'location',
                     'address', 'url', 'date_fetched']

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for listing in listings:
                    row = {field: listing.get(field, '') for field in fieldnames}
                    writer.writerow(row)

            logger.info(f"Saved {len(listings)} listings to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")
            return None

    def save_json(self, listings: List[Dict[str, Any]], filename: str = None) -> str:
        """Save listings to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'listings_{timestamp}.json'

        filepath = self.output_dir / filename

        try:
            # Remove raw_data for cleaner JSON
            clean_listings = []
            for listing in listings:
                clean = {k: v for k, v in listing.items() if k != 'raw_data'}
                clean_listings.append(clean)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(clean_listings, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved {len(listings)} listings to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            return None

    def print_summary(self, listings: List[Dict[str, Any]], summary: Dict[str, Any]):
        """Print summary to console"""
        safe_print("\n" + "=" * 60)
        safe_print("APARTMENT SEARCH RESULTS")
        safe_print("=" * 60)
        safe_print(f"Total listings found: {summary['total']}")

        if summary['total'] > 0:
            safe_print(f"\nListings by source:")
            for source, count in summary.get('by_source', {}).items():
                safe_print(f"  • {source}: {count}")

            price_min = summary.get('price_min')
            price_max = summary.get('price_max')
            price_avg = summary.get('price_avg')

            if price_min:
                safe_print(f"\nPrice range: ILS {price_min:,.0f} - ILS {price_max:,.0f}")
                safe_print(f"Average price: ILS {price_avg:,.0f}")

        safe_print("\n" + "=" * 60)
        safe_print("First 10 listings:")
        safe_print("=" * 60)

        for i, listing in enumerate(listings[:10], 1):
            safe_print(f"\n{i}. {listing.get('title', 'N/A')}")
            safe_print(f"   Price: ILS {listing.get('price', 'N/A')}")
            safe_print(f"   Rooms: {listing.get('rooms', 'N/A')} | Area: {listing.get('area', 'N/A')} m²")
            safe_print(f"   Location: {listing.get('address', listing.get('location', 'N/A'))}")
            safe_print(f"   Source: {listing.get('source', 'N/A')}")
            safe_print(f"   URL: {listing.get('url', 'N/A')}")

        if len(listings) > 10:
            safe_print(f"\n... and {len(listings) - 10} more listings")

        safe_print("\n" + "=" * 60)
