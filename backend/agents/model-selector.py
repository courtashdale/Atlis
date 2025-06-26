# backend/agents/model_selector.py
from common.oa_agent import run_agent

input = "Find one important geopolitical event from the past 24 hours."

model = run_agent(
    system_message="You are an expert model selector. Your job is to choose the best AI model from the list for a given task, and return ONLY the model name string (e.g., 'gpt-4o-mini-search-preview-2025-03-11'). Do not explain or include anything else.",
    user_prompt=f"""Given the prompt below, return the best model name (as a string) to handle it. The available models are defined in the schema. Return only the model string.

Prompt: ###{input}###
""",
    schema_path="../schema/model_string.schema.json",
    model="gpt-4o-mini"
)

print(model)