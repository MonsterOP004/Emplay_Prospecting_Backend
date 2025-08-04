import requests
from dotenv import load_dotenv
import os
load_dotenv(override=True)

perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

url = "https://api.perplexity.ai/chat/completions"
headers = {
    "Authorization": f"Bearer {perplexity_api_key}",  # Replace with your actual API key
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "user", "content": "What were the results of the 2025 French Open Finals?"}
    ]
}

# Make the API call
response = requests.post(url, headers=headers, json=payload)

# Print the AI's response
print(response.json())