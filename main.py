# main.py

from scripts.scrape_articles import fetch_articles, save_articles  
from scripts.utils import compute_article_hashes

from dotenv import load_dotenv

HASH_RECORD_FILE = "article_hashes.json"  # To track previous hashes

load_dotenv()

def main():
  # scrape articles
  print("Scraping articles...")
  articles = fetch_articles()
  save_articles(articles, articles_dir="articles")

  # compute hashes
  print("Checking for new or updated articles...")
  current_hashes = compute_article_hashes()
  print(current_hashes)
if __name__ == "__main__":
  main()