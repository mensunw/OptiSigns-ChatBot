# main.py

import os
from scripts.scrape_articles import fetch_articles, save_articles  
from scripts.upload_to_openai import upload_file
from scripts.utils import compute_article_hashes, load_json, detect_changes, log_results, save_json #, delete_all_openai_files

from dotenv import load_dotenv

# for tracking previous hashes
OLD_HASH_FILE = "article_hashes.json"

load_dotenv()

def main():
  #delete_all_openai_files()
  
  try:
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

    # upload added/updated articles
    if added or updated:
      print(f"Uploading {len(added) + len(updated)} new/updated articles...")
      # go through each added/updated article and upload them
      for filename in added + updated:
        filepath = os.path.join("articles", filename)
        file_id = upload_file(filepath)
        print(f"Uploaded {filename} as file_id {file_id}")
    else:
      print("No new or updated articles to upload.")

    # save current hash and old hash now
    save_json(current_hashes)
    
    # log the changes
    log_results(added,updated,skipped)
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    

if __name__ == "__main__":
  main()