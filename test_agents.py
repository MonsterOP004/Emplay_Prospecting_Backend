import requests

# URL of your backend endpoint
url = "http://localhost:8000/prospecting_node"

# Example request payload
payload = {
    "agent_name": "Product Research",
    "user_input": "We are launching a fitness tracking wearable for Indian college students. Price is ₹2999, subscription-based model with access to AI-driven analytics and wellness tips."
}

# Send POST request to backend
try:
    response = requests.post(url, json=payload)

    # Display the result
    if response.status_code == 200:
        print("[SUCCESS] Agent Response:")
        print(response.json())
    else:
        print(f"[ERROR] Status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"[EXCEPTION] {e}")
