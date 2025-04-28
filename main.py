# main.py

from scripts.scrape_articles import fetch_articles, save_articles  

from dotenv import load_dotenv

load_dotenv()

def main():
    # scrape articles
    print("Scraping articles...")
    articles = fetch_articles()
    save_articles(articles, articles_dir="articles")
    
if __name__ == "__main__":
    main()