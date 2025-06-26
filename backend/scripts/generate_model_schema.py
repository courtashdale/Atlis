# backend/scripts/generate_model_schema.py

import json

with open("backend/data/models.json", "r") as f:
    data = json.load(f)

models = []
for group in data.values():
    for model in group["models"]:
        models.append(model["model"])

schema = {
    "type": "object",
    "properties": {
        "model": {
            "type": "string",
            "enum": sorted(set(models))
        }
    },
    "required": ["model"]
}

with open("backend/schema/model_string.schema.json", "w") as f:
    json.dump(schema, f, indent=2)

# run:
# python scripts/generate_model_schema.py