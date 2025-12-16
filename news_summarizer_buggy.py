import os
import requests
import argparse
from dotenv import load_dotenv
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL_EVERYTHING = "https://newsapi.org/v2/everything"
BASE_URL_TOP = "https://newsapi.org/v2/top-headlines"

def get_articles(keyword=None, from_date=None, to_date=None):
    if not API_KEY:
        print("Error: NEWS_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        return []

    params = {
        "apiKey": API_KEY,
        "language": "en",
        "sortBy": "publishedAt"
    }

    # Determine endpoint and parameters based on input
    if keyword or from_date or to_date:
        url = BASE_URL_EVERYTHING
        if keyword:
            params["q"] = keyword
        else:
            # 'everything' endpoint requires 'q' parameter usually, but sometimes 'domains' etc.
            # If no keyword is provided but dates are, we might need a general query or fallback.
            # Let's default to a broad query if only dates are provided to avoid API error,
            # or just use top-headlines if no keyword.
            # Actually, the requirement allows filtering by date range.
            # If user asks for date range without keyword, 'top-headlines' doesn't support date filtering well in free tier (only 'everything' does).
            # So we must use 'everything'. We will set q='news' or similar if missing, or enforce keyword.
            # Let's enforce keyword if using 'everything' endpoint to be safe, or default to "general".
            if not keyword:
                params["q"] = "general"
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
    else:
        url = BASE_URL_TOP
        params["source"] = "bbc-news" # Keeping original behavior logic
        # if source is specified, category/country cannot be mixed in v2 usually.
        # But 'source=bbc-news' is valid for top-headlines.

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx, 5xx)
        
        data = response.json()
        if data.get("status") != "ok":
            print(f"API returned error: {data.get('message')}")
            return []
            
        return data.get("articles", [])

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except ValueError:
        print("Error parsing JSON response.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def summarize(articles):
    if not articles:
        print("No articles found to summarize.")
        return

    print(f"Found {len(articles)} articles:\n")
    for art in articles:
        print("Title:", art.get('title', 'N/A'))
        print("Description:", art.get('description', 'N/A'))
        print("URL:", art.get('url', 'N/A'))
        print("----")


def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Please use YYYY-MM-DD.")

def main():
    parser = argparse.ArgumentParser(description="News Summarizer with Filtering")
    parser.add_argument("-k", "--keyword", help="Filter news by keyword")
    parser.add_argument("--from", dest="from_date", type=validate_date, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", type=validate_date, help="End date (YYYY-MM-DD)")
    
    args = parser.parse_args()

    # Basic date validation logic (start <= end)
    if args.from_date and args.to_date:
        if args.from_date > args.to_date:
            print("Error: Start date cannot be after end date.")
            return

    print("Fetching news...")
    articles = get_articles(keyword=args.keyword, from_date=args.from_date, to_date=args.to_date)
    summarize(articles)


if __name__ == "__main__":
    main()
