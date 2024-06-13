import sys
import json
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import requests


def stdout_write(openrouter_api_key_and_names):
    """Writes the response to stdout."""
    response_dict = {
        "variables": {
            "request": "Requesting data…",
        },
        "items": [
            {
                "uid": "null",
                "type": "default",
                "title": f"{round(res['limit_remaining'] / res['limit'] * 100, 1)}% left for key ‘{name}’: ‘{res['label']}’" if "error_status_code" not in res else f"Error fetching OpenRouter credit usage: {res['error_status_code']}",
                "subtitle": f"${round(res['usage'], 3)} used in ${res['limit']}" if "error_status_code" not in res else f"{res['error_response_text']}",
                "arg": "",
                "autocomplete": "",
                "icon": {"path": "./icon.png"},
            } for name, res in {
                name: fetch_openrouter_credit_usage_for_key(key)
                for name, key in openrouter_api_key_and_names.items()
            }.items()
        ]
    }

    sys.stdout.write(json.dumps(response_dict))


def fetch_openrouter_credit_usage_for_key(openrouter_key):
    usage_url = "https://openrouter.ai/api/v1/auth/key"

    headers = {
        'Authorization': f"Bearer {openrouter_key}",
    }

    response = requests.get(usage_url, headers=headers)

    if response.status_code == 200:
        return response.json()["data"]
    else:
        return {
            'error_status_code': response.status_code,
            'error_response_text': response.text,
        }


if __name__ == '__main__':
    openrouter_api_keys_and_names = sys.argv[1]
    tem_ll = [kn.strip() for kn in openrouter_api_keys_and_names.split(";") if kn]
    dict_of_api_keys_and_names = {k.strip(): v.strip() for k, v in [kv.split(":") for kv in tem_ll] if v.strip() and k.strip()}

    stdout_write(dict_of_api_keys_and_names)
