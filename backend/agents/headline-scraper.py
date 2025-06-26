# backend/agents/headline-scraper.py
from common.oa_agent import run_agent

article = run_agent(
    system_message="You are a geopolitical analyst.",
    user_prompt="Find five important geopolitical events from the past 24 hours.",
    schema_path="../schema/article.json"
)

print(article)