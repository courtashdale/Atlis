# backend/agents/headline-scraper.py
from common.oa_agent import run_agent

current_events = run_agent(
    system_message="You are a geopolitical analyst.",
    user_prompt="List 5 headline geopolitical events or current geopolitical developments that most analysts should be aware of. Return the result as an array of strings under the key 'events'.",
    schema_path="../schema/hot_topics.json"
)

# Print each headline
for event in current_events["events"]:
    print("🔹", event)