import sys
import json
import os
from decimal import Decimal

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import requests


def stdout_write(data_list):
    """Writes the response to stdout."""
    response_dict = {
        "items": [
            {
                "uid": "null",
                "type": "default",
                "title": f"{model_item['id']}, context {'{:,}'.format(model_item['context_length'])}",
                "subtitle": f"Priced ${(Decimal(model_item['pricing']['prompt']) * 1000).normalize()}/1k for prompt, ${(Decimal(model_item['pricing']['completion']) * 1000).normalize()}/1k for completion, press ↩ to copy model name",
                "arg": model_item['id'],
                "autocomplete": model_item['id'],
                "icon": {"path": "./icon.png"}
            } for model_item in data_list
        ]
    }
    sys.stdout.write(json.dumps(response_dict))


def fetch_openapi_usage_statistics():
    url = "https://openrouter.ai/api/v1/models"

    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response and extract all models
        data_list = response.json()["data"]

        return data_list
    else:
        print(
            f"Error fetching OpenRouter available models: {response.status_code} - {response.text}"
        )
        return


if __name__ == '__main__':
    stdout_write(fetch_openapi_usage_statistics())
    