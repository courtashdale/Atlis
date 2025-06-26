# sandbox/events_plus_articles.py
from backend.agents.common.oa_agent import run_agent
import os
import requests
from dotenv import find_dotenv, load_dotenv
from datetime import date
from newsapi import NewsApiClient

# Load API Key
_ = load_dotenv(find_dotenv())
key = os.getenv("NEWS_API_KEY")
if not key:
    raise ValueError("Couldn't find the API key!")

# Initialize NewsAPI
newsapi = NewsApiClient(api_key=key)
today = str(date.today())

# Get current event topics
current_events = run_agent(
    system_message="You are a geopolitical analyst.",
    user_prompt=(
        "List 5 current geopolitical topics, changes, or conflicts that analysts should be aware of. ",
        "Eech event should be represented by **up to three keywords**, separated by 'AND'. ",
        "Examples: 'Israel AND Gaza AND Ceasefire', 'Russia AND NATO', 'China AND Taiwan AND Tensions'. ",
        "Return this as an array under the key 'events'."
    ),
    schema_path="../schema/hot_topics.json"
)

# Print each headline
for event in current_events["events"]:
    print(f"\n🔍 Searching for articles about: {event}\n")
    try:
        all_articles = newsapi.get_everything(
            q=event,
            from_param='2025-06-20',
            to=today,
            language='en',
            sort_by='relevancy',
            page_size=10,
            page=1
        )
        for article in all_articles.get('articles', []):
            print("🔹", article['url'])
    except Exception as e:
        print(f"❌ Couldn't find articles about {event}: {e}")