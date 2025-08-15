import requests
import json

BASE_URL = "http://localhost:6969"

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
print(res.status_code, res.json())

# Step 5: Select strategies
strategy_selection = {
    "selected_strategy_ids": ["social_media_marketing", "local_awareness"],
    "month_activity_selections": {
        "1": ["Instagram launch campaign", "Facebook ad boost"]
    }
}
print("\n=== Step 5: Selecting Strategies ===")
res = requests.post(f"{BASE_URL}/get_selected_strategy/{plan_id}", json=strategy_selection)
print(res.status_code, res.json())

# Step 6: Generate final expanded plan
print("\n=== Step 6: Generating Final Plan ===")
res = requests.post(f"{BASE_URL}/generate_final_plan/{plan_id}")
print(res.status_code, json.dumps(res.json(), indent=2))
