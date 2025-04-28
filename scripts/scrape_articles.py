# scripts/scrape_articles.py

import os
import requests
import re
from dotenv import load_dotenv
from markdownify import markdownify as md

load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN") 

def fetch_articles():
    """
    Fetch article list using Zendesk API
    """
    url = f"https://{ZENDESK_SUBDOMAIN}/api/v2/help_center/en-us/articles.json" # conventional zendesk api endpoint for articles (GET /api/v2/help_center/{locale}/articles)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['articles']

def parse_title(title):
    """
    Parses title for unwanted characters
    """
    slug = title.lower()
    # replace anything NOT a word character or hyphen with a hyphen
    slug = re.sub(r"[^\w\-]", "-", slug) 
    # replace multiple hyphens with a single hyphen 
    slug = re.sub(r"-+", "-", slug)
    # remove leading/trailing hyphens        
    slug = slug.strip("-")               
    return slug  

def html_to_markdown(html_content):
    """
    Convert HTML into clean Markdown
    """
    return md(html_content, strip=["nav", "footer", "header", "aside"]) # "aside" usually contains ads

def save_articles(articles, articles_dir="../articles"):
    """
    Save the articles after cleaning
    """

    # might delete the directory for easy reset
    if not os.path.exists(articles_dir):
        os.makedirs(articles_dir)

    # convert them to md and save them
    for article in articles:
        slug = parse_title(article['title'])
        html_body = article['body']
        markdown_text = html_to_markdown(html_body)

        filepath = os.path.join(articles_dir, f"{slug}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        print(f"Saved {filepath}")
    

def main():
    try:
        # fetch articles
        articles = fetch_articles()
        print(f"Fetched {len(articles)} articles.")
        # save the articles
        save_articles(articles)
        print(f"Saved the articles.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
