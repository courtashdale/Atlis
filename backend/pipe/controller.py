# backend/pipe/controller.py
from agents.headline_scraper import get_articles
from helpers.filter import filter_verified_articles
import json
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        raw_articles = get_articles()
        articles = raw_articles if isinstance(raw_articles, list) else [raw_articles]

        verified = filter_verified_articles(articles, reputable_json_path="../data/reputable.json")
        
        print(json.dumps(verified, indent=2))
    except Exception as e:
        logging.error(f"Issue running controller pipeline: {e}")

if __name__ == "__main__":
    main()