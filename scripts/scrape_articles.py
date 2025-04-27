# scripts/scrape_articles.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN") 

HEADERS = {
  "Authorization": f"Basic {os.getenv('ZENDESK_AUTH')}"
}

ARTICLES_DIR = "../articles" 

def fetch_articles():
    """
    Fetch article list using Zendesk API.
    """
    url = f"https://{ZENDESK_SUBDOMAIN}/api/v2/help_center/en-us/articles.json" # conventional zendesk api endpoint for articles
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data['articles']

def main():
    try:
      articles = fetch_articles()
      print(articles)
      print(f"Fetched {len(articles)} articles.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
