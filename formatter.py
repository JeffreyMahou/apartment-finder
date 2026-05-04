import csv
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


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
        print("\n" + "=" * 60)
        print("APARTMENT SEARCH RESULTS")
        print("=" * 60)
        print(f"Total listings found: {summary['total']}")

        if summary['total'] > 0:
            print(f"\nListings by source:")
            for source, count in summary.get('by_source', {}).items():
                print(f"  • {source}: {count}")

            price_min = summary.get('price_min')
            price_max = summary.get('price_max')
            price_avg = summary.get('price_avg')

            if price_min:
                print(f"\nPrice range: ₪{price_min:,.0f} - ₪{price_max:,.0f}")
                print(f"Average price: ₪{price_avg:,.0f}")

        print("\n" + "=" * 60)
        print("First 10 listings:")
        print("=" * 60)

        for i, listing in enumerate(listings[:10], 1):
            print(f"\n{i}. {listing.get('title', 'N/A')}")
            print(f"   Price: ₪{listing.get('price', 'N/A')}")
            print(f"   Rooms: {listing.get('rooms', 'N/A')} | Area: {listing.get('area', 'N/A')} m²")
            print(f"   Location: {listing.get('address', listing.get('location', 'N/A'))}")
            print(f"   Source: {listing.get('source', 'N/A')}")
            print(f"   URL: {listing.get('url', 'N/A')}")

        if len(listings) > 10:
            print(f"\n... and {len(listings) - 10} more listings")

        print("\n" + "=" * 60)
