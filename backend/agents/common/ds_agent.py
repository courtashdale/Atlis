# backend/agents/common/ds-agent.py
"""
This is a boilerplate LLM agent that accepts:
- A system message
- A user prompt
- A JSON schema path

It handles:
- Injecting the schema into the prompt (delimited with ###)
- Sending the request to the LLM (DeepSeek compatible)
- Parsing and validating the result

Returns: a validated Python dict or raises clear errors.
"""

import os
import json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from jsonschema import validate as jsonschema_validate, ValidationError as JsonSchemaValidationError

# Load .env
_ = load_dotenv(find_dotenv())
key = os.getenv("DS_KEY")

# Initialize DeepSeek-compatible client
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")


def run_agent(
    *,
    system_message: str,
    user_prompt: str,
    schema_path: str,
    model: str = "deepseek-chat"
) -> Dict[str, Any]:
    """Run a prompt against the model with schema validation."""

    # Resolve absolute path to schema
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abs_schema_path = os.path.join(base_dir, schema_path)

    with open(abs_schema_path, "r") as f:
        schema = json.load(f)

    schema_str = json.dumps(schema, indent=2)

    # Inject schema with triple-### delimiters
    full_prompt = f"""
{user_prompt}

Use the following schema:
###json
{schema_str}
###

Only return a valid JSON object. Do not include markdown or explanations.
"""

    # Send request to model
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": full_prompt}
        ],
        stream=False
    )

    # Parse and validate output
    try:
        output_raw = response.choices[0].message.content.strip()
        data = json.loads(output_raw)
        jsonschema_validate(instance=data, schema=schema)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ JSON parsing error:\n{e}\nRaw output:\n{output_raw}") from e
    except JsonSchemaValidationError as e:
        raise ValueError(f"❌ Schema validation failed:\n{e.message}\nRaw output:\n{output_raw}") from e