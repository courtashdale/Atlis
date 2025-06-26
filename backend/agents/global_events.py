# backend/agents/global_events.py
from common.oa_agent import run_agent

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Now your imports work
from backend.agents.common.oa_agent import run_agent

current_events = run_agent(
    system_message="You are a geopolitical analyst.",
    user_prompt="List 5 headline geopolitical events or current geopolitical developments that most analysts should be aware of. Return the result as an array of strings under the key 'events'.",
    schema_path="hot_topics.json"
)

# Print each headline
print(f"📰 Five headlines of current events: \n")
for event in current_events["events"]:
    print("🔹", event)