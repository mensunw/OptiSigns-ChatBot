# scripts/scrape_articles.py

import os
import requests
from dotenv import load_dotenv
from markdownify import markdownify as md

load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN") 

ARTICLES_DIR = "../articles" 

def fetch_articles():
    """
    Fetch article list using Zendesk API
    """
    url = f"https://{ZENDESK_SUBDOMAIN}/api/v2/help_center/en-us/articles.json" # conventional zendesk api endpoint for articles
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['articles']

def html_to_markdown(html_content):
    """
    Convert HTML into clean Markdown
    """
    return md(html_content, strip=["nav", "footer", "header", "aside"]) # "aside" usually contains ads

def save_markdown(slug, markdown_text):
    """
    Save the cleaned markdown to a file
    """

    # might delete the directory for easy reset
    if not os.path.exists(ARTICLES_DIR):
        os.makedirs(ARTICLES_DIR)

    filepath = os.path.join(ARTICLES_DIR, f"{slug}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"Saved {filepath}")

def main():
    try:
      # fetch articles
      articles = fetch_articles()
      print(f"Fetched {len(articles)} articles.")

      # convert them to md and save them
      for article in articles:
        slug = article['title'].lower().replace(" ", "-").replace("/", "-").replace("?", "-") # may need to include other characters later
        html_body = article['body']
        markdown_text = html_to_markdown(html_body)
        save_markdown(slug, markdown_text)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
