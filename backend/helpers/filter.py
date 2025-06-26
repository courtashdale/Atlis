# backend/helpers/filter.py

"""
This function filters a list of JSON objects from headline_scraper.py to clean out unreputable sources.
"""

import json
from datetime import datetime, timedelta

def filter_verified_articles(articles, reputable_json_path):
    with open(reputable_json_path, "r") as f:
        reputable_domains = set(domain.lower().strip() for domain in json.load(f))

    cutoff_time = datetime.utcnow() - timedelta(hours=72)

    verified_articles = []
    for article in articles:
        try:
            domain = article["source"]["domain"].lower().strip()
            published_at = datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))
            if domain in reputable_domains and published_at >= cutoff_time:
                verified_articles.append(article)
        except (KeyError, ValueError, TypeError):
            continue  # Skip malformed articles

    return verified_articles