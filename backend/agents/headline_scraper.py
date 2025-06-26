# backend/agents/headline_scraper.py
from agents.common.oa_agent import run_agent

def get_articles():
    result = run_agent(
        system_message="You are a geopolitical analyst.",
        user_prompt=f"""Find five important geopolitical events from the past 48 hours.

        When listing country_mentions for international organizations (e.g. NATO, EU, ASEAN), do not expand them into full member lists unless the article explicitly discusses specific member states.

        Only include a country in country_mentions if it is named directly in the article or plays a clear, specific role in the event.
        
        """,
        schema_path="article.json"
    )

    return result or []

if __name__ == "__main__":
    articles = get_articles()
    print(articles)