#!/usr/bin/env python3
import argparse
import sys
import logging
from scrapers.yad2_scraper import Yad2Scraper
from scrapers.madlan_scraper import MadlanScraper
from aggregator import ListingAggregator
from formatter import ListingFormatter
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Israeli Apartment Finder - Aggregate listings from Yad2 and Madlan')
    parser.add_argument('--location', default=config.DEFAULT_LOCATION, help='City/location to search')
    parser.add_argument('--min-price', type=int, default=config.MIN_PRICE, help='Minimum price in ILS')
    parser.add_argument('--max-price', type=int, default=config.MAX_PRICE, help='Maximum price in ILS')
    parser.add_argument('--min-rooms', type=int, default=config.MIN_ROOMS, help='Minimum number of rooms')
    parser.add_argument('--max-rooms', type=int, default=config.MAX_ROOMS, help='Maximum number of rooms')
    parser.add_argument('--format', choices=['csv', 'json'], default=config.OUTPUT_FORMAT, help='Output format')
    parser.add_argument('--no-save', action='store_true', help='Don\'t save to file')
    parser.add_argument('--yad2-only', action='store_true', help='Only search Yad2')
    parser.add_argument('--madlan-only', action='store_true', help='Only search Madlan')

    args = parser.parse_args()

    # Validate API token
    if not config.APIFY_API_TOKEN:
        logger.error("APIFY_API_TOKEN not set. Please set it in .env file.")
        logger.error("Sign up at https://apify.com and get your API token.")
        sys.exit(1)

    logger.info(f"Searching for apartments in {args.location}")
    logger.info(f"Price range: ₪{args.min_price:,} - ₪{args.max_price:,}")
    logger.info(f"Rooms: {args.min_rooms} - {args.max_rooms}")

    # Initialize scrapers
    yad2_listings = []
    madlan_listings = []

    if not args.madlan_only:
        logger.info("Fetching from Yad2...")
        yad2 = Yad2Scraper(config.APIFY_API_TOKEN)
        yad2_listings = yad2.fetch_listings(
            args.location, args.min_price, args.max_price,
            args.min_rooms, args.max_rooms
        )

    if not args.yad2_only:
        logger.info("Fetching from Madlan...")
        madlan = MadlanScraper(config.APIFY_API_TOKEN)
        madlan_listings = madlan.fetch_listings(
            args.location, args.min_price, args.max_price,
            args.min_rooms, args.max_rooms
        )

    # Aggregate listings
    aggregator = ListingAggregator()
    all_listings = aggregator.aggregate(yad2_listings, madlan_listings)
    summary = aggregator.get_summary(all_listings)

    # Format output
    formatter = ListingFormatter(config.OUTPUT_DIR)
    formatter.print_summary(all_listings, summary)

    # Save to file if requested
    if not args.no_save and config.SAVE_TO_FILE:
        if args.format == 'csv':
            filepath = formatter.save_csv(all_listings)
            logger.info(f"Results saved to: {filepath}")
        elif args.format == 'json':
            filepath = formatter.save_json(all_listings)
            logger.info(f"Results saved to: {filepath}")

    return 0 if all_listings else 1


if __name__ == '__main__':
    sys.exit(main())
