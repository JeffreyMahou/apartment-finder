# Israeli Apartment Finder

Aggregate apartment listings from Yad2 and Madlan into a single, easy-to-review CSV file.

## Setup

### 1. Get Apify API Token

1. Sign up at https://apify.com (free tier available)
2. Go to your account settings and copy your API token
3. Create a `.env` file in this directory and add:
   ```
   APIFY_API_TOKEN=your_token_here
   ```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Search Parameters

Edit `.env` file to set your search criteria:
```
DEFAULT_LOCATION=Tel Aviv
MIN_PRICE=1000
MAX_PRICE=5000
MIN_ROOMS=1
MAX_ROOMS=4
```

## Usage

### Basic search with default parameters:
```bash
python main.py
```

### Search with custom parameters:
```bash
python main.py --location "Tel Aviv" --min-price 2000 --max-price 4000 --min-rooms 2
```

### Search only Yad2 or Madlan:
```bash
python main.py --yad2-only
python main.py --madlan-only
```

### Save as JSON instead of CSV:
```bash
python main.py --format json
```

### Don't save to file (print to console only):
```bash
python main.py --no-save
```

## Output

Results are saved to the `data/` folder as:
- `listings_YYYYMMDD_HHMMSS.csv` (default)
- `listings_YYYYMMDD_HHMMSS.json` (if --format json)

The CSV includes:
- Source (Yad2 or Madlan)
- Title
- Price (ILS)
- Rooms
- Area (m²)
- Location
- Address
- URL
- Date fetched

## How It Works

1. **Fetch**: Queries Yad2 and Madlan APIs via Apify
2. **Standardize**: Converts data from both sources to a consistent format
3. **Deduplicate**: Removes listings that appear on multiple platforms
4. **Sort**: Sorts by price (lowest first)
5. **Save**: Exports to CSV or JSON

## Troubleshooting

### API errors?
- Check that your Apify token is valid
- Ensure you have API credits (free accounts get trial credits)
- Check your search location spelling

### No results?
- Try expanding price/rooms range
- Try a different location
- Check Apify console to debug API calls

## Future Enhancements

- Add Facebook Marketplace/Groups support
- Schedule automatic daily/weekly searches
- Email/Slack notifications for new listings
- Filter by amenities, building age, etc.
