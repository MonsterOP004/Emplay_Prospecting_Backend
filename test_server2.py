import requests
import json

BASE_URL = "https://bb5c4eba7f26.ngrok-free.app"

# Step 1: Send basic business info
business_info = {
    "business_name": "Willow and Rose Makeup",
    "business_type": "Professional Makeup Studio",
    "location": "Surrey, UK",
    "website_link": "https://www.willowandrosemakeup.co.uk/about",
    "business_goals": "Increase sales by 20%, grow Instagram followers by 5,000, boost web traffic by 20%",
    "marketing_budget": 1500.0,
    "target_audience": "Brides-to-be, Event Attendees, Local Professionals",
    "current_marketing_assets": "Instagram, Facebook, Website",
    "brand_voice": "Professional, Creative, Friendly"
}

res = requests.get(f"{BASE_URL}/delete_all_plans")
print(res.status_code, res.json())

print("\n=== Step 1: Storing Business Info ===")
res = requests.post(f"{BASE_URL}/user_basic_input", json=business_info)
print(res.status_code, res.json())
plan_id = res.json()["plan_id"]

# Step 2: Call Perplexity
print("\n=== Step 2: Calling Perplexity ===")
res = requests.post(f"{BASE_URL}/call_perplexity/{plan_id}", json=business_info)
print(res.status_code, res.json())
perplexity_data = res.json().get("perplexity_data", {})

# Step 3: Fill missing Perplexity info (simulate)
missing_data = {
    "company_research": {
        "products_services": ["Bridal makeup", "Event makeup", "Workshops"],
        "unique_selling_points": ["Custom looks", "Luxury products", "Mobile service"]
    }
}
print("\n=== Step 3: Updating Missing Info ===")
res = requests.post(f"{BASE_URL}/get_missing_info/{plan_id}", json=missing_data)
print(res.status_code, res.json())

# Step 4: Generate marketing plan
print("\n=== Step 4: Generating Marketing Plan ===")
res = requests.post(f"{BASE_URL}/generate_marketing_plan/{plan_id}")
print(res.status_code, json.dumps(res.json(), indent=2))

# Step 5: Chat loop with agent
print("\n=== Step 5: Chatting with Agent ===")
print("Type 'exit' to end the conversation.\n")

while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit", "q"]:
        print("👋 Ending chat with agent.")
        break
    
    res = requests.post(
        f"{BASE_URL}/chat_with_agent/{plan_id}",
        json={"message": user_message}
    )
    
    if res.status_code == 200:
        data = res.json()
        print("\nAgent:", data.get("refined_plan", "No response"))
    else:
        print("❌ Error:", res.status_code, res.text)
