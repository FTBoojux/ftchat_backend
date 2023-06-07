import requests
import json

from ftchat.applicationConf import openai_api_key as api_key

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

def send_to_gpt(msg,model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": msg}],
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(data),
        proxies=proxies
    )

    return response.json()