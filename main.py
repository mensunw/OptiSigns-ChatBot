# main.py

import os
from scripts.scrape_articles import fetch_articles, save_articles  
from scripts.utils import compute_article_hashes, load_json, detect_changes, log_results, save_json

from dotenv import load_dotenv

# for tracking previous hashes
OLD_HASH_FILE = "article_hashes.json"

load_dotenv()

def main():
  # scrape articles
  print("Scraping articles...")
  articles = fetch_articles()
  save_articles(articles, articles_dir="articles")
  
  # compute hashes
  print("Checking for new or updated articles...")
  current_hashes = compute_article_hashes()
  
  # for deleting/resetting hash file purposes
  if os.path.exists(OLD_HASH_FILE):
    old_hashes = load_json()
  else:
    old_hashes = {}
  
  # check for changes and see if any articles added, updated, or skipped
  added, updated, skipped = detect_changes(old_hashes, current_hashes)

  # upload new/updated articles

  # save current hash and old hash now
  save_json(current_hashes)
  
  # log the changes
  log_results(added,updated,skipped)
  

if __name__ == "__main__":
  main()