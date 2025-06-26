# backend/agents/model_selector.py
import json
import time
from pathlib import Path
from common.oa_agent import run_agent
import tiktoken

# Load model metadata
with open(Path(__file__).parent.parent / "data" / "models.json") as f:
    MODEL_DB = json.load(f)

def get_model_metadata(model_name: str) -> dict:
    for category in MODEL_DB.values():
        for model in category["models"]:
            if model["model"] == model_name:
                return model
    return {}

def estimate_token_cost(prompt: str, model_name: str) -> tuple[float, int]:
    enc = tiktoken.encoding_for_model(model_name if "gpt" in model_name else "gpt-4")
    tokens = len(enc.encode(prompt))
    meta = get_model_metadata(model_name)
    cost_per_1k = meta.get("input_cost", 0)
    return round((tokens / 1000) * cost_per_1k, 4), tokens

def select_best_model(user_prompt: str) -> str:
    print("⚖️ Choosing the best model...")
    start_total = time.time()

    # Step 1: Estimate cost
    start = time.time()
    preview_model = "gpt-4o-mini"
    prompt_text = f"""Given the task described in this prompt, return the best model from the list.

Prompt:
{user_prompt}

Only return the model name as a JSON object like: {{ "model": "<model-name>" }}
"""
    cost, tokens = estimate_token_cost(prompt_text, preview_model)
    print(f"💰 Est. model selection cost: ${cost} ({tokens} tokens @ {preview_model})")
    print(f"⏱️ Cost estimate took {round(time.time() - start, 3)}s")

    # Step 2: Run selector agent
    start = time.time()
    result = run_agent(
        system_message="You are an expert model selector. Your job is to choose the best AI model for the given task. Return ONLY the model name string (e.g., 'gpt-4o-mini-search-preview-2025-03-11').",
        user_prompt=prompt_text,
        schema_path="../schema/model_string.schema.json",
        model=preview_model
    )
    print(f"⏱️ LLM selection took {round(time.time() - start, 3)}s")

    # Step 3: Final report
    start = time.time()
    model = result["model"]
    shorthand = get_model_metadata(model).get("shorthand", "—")
    print(f"▶︎ Model: {model} ({shorthand})")
    print(f"⏱️ Final metadata lookup took {round(time.time() - start, 3)}s")

    print(f"⏱️ Total selector time: {round(time.time() - start_total, 3)}s")
    return model