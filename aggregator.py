import difflib
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ListingAggregator:
    def __init__(self, similarity_threshold: float = 0.95):
        self.similarity_threshold = similarity_threshold

    def aggregate(self, *listing_lists: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Combine listings from multiple sources"""
        all_listings = []
        for listings in listing_lists:
            all_listings.extend(listings)

        logger.info(f"Total listings before deduplication: {len(all_listings)}")
        deduplicated = self._deduplicate(all_listings)
        logger.info(f"Total listings after deduplication: {len(deduplicated)}")

        return self._sort_listings(deduplicated)

    def _deduplicate(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate listings using fuzzy address matching"""
        unique_listings = []
        seen_addresses = []

        for listing in listings:
            address = listing.get('address', '').lower().strip()
            price = listing.get('price')

            # Check if this listing is a duplicate
            is_duplicate = False
            for seen_addr in seen_addresses:
                similarity = difflib.SequenceMatcher(None, address, seen_addr).ratio()
                if similarity > self.similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_listings.append(listing)
                seen_addresses.append(address)

        removed = len(listings) - len(unique_listings)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate listings")

        return unique_listings

    def _sort_listings(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort listings by price (ascending)"""
        return sorted(listings, key=lambda x: x.get('price', float('inf')))

    def get_summary(self, listings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics"""
        if not listings:
            return {'total': 0}

        prices = [l.get('price') for l in listings if l.get('price')]
        sources = {}
        for listing in listings:
            source = listing.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1

        return {
            'total': len(listings),
            'by_source': sources,
            'price_min': min(prices) if prices else None,
            'price_max': max(prices) if prices else None,
            'price_avg': sum(prices) / len(prices) if prices else None,
        }
