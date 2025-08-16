# openai_client.py
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def call_openai_tool(business_info, perplexity_data):

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    business_name = business_info.get("business_name", "Unknown")
    business_type = business_info.get("business_type", "Unknown")
    location = business_info.get("location", "Unknown")
    website_link = business_info.get("website_link", "Unknown")
    business_goals = business_info.get("business_goals", "Unknown")
    marketing_budget = business_info.get("marketing_budget", "Unknown")
    target_audience = business_info.get("target_audience", "Unknown")
    current_marketing_assets = business_info.get("current_marketing_assets", "Unknown")
    brand_voice = business_info.get("brand_voice", "Unknown")

    research_context = json.dumps(perplexity_data, indent=2)

    system_message = f"""
        12-Month Marketing Plan with Execution Pathway (Perplexity-Optimized)

        Create a detailed 12-month marketing plan for the following business:

        Business Name: {business_name}
        Business Type: {business_type}
        Location: {location}
        Business Goals: {business_goals}
        Brand Voice: {brand_voice}
        Website: {website_link}
        Marketing Budget: {marketing_budget}
        Target Audience: {target_audience}
        Current Marketing Assets: {current_marketing_assets}

        Perplexity Research Data:
        {research_context}

        Instructions:
        Leverage Perplexity research findings (company, competitor, benchmarks, best channels, seasonality, cultural hooks).
        Integrate insights into actionable recommendations — do not repeat raw Perplexity data; synthesize into strategies and execution steps.
        If Perplexity data is missing for any of the following, ask optionally (do not block progress):

        - Target audience nuances
        - Key markets to prioritize
        - Seasonal/cultural moments
        - Approx. monthly marketing budget (£)

        Plan Format & Headings

        1. Business & Brand Positioning
            • Goal: [1–2 sentences based on Perplexity + user input]
            • Target Audience: [3–5 segments]
            • Brand Voice: [1 short sentence]

        2. Marketing Objectives (12 months)
            • List 3–5 measurable objectives with specific targets (e.g., % increase in traffic, lead conversions, revenue).

        3. Core Strategies
        Present in a Markdown table with columns:

        | Strategy Area                  | Tactics |
        |--------------------------------|---------|
        | Local Awareness & Community Presence | 3+ tactics, each with a “how-to” and USP leveraged |
        | Social Media Marketing | For each recommended platform: <br>• 2+ weekly content themes <br>• Campaign ideas tied to USPs & seasonal/cultural events <br>• Formats (carousel, reel, video, static, live) <br>• Posting frequency <br>• Core message/positioning |
        | Loyalty & Retention | 3+ tactics |
        | Email Marketing | 3+ tactics |
        | SMS/WhatsApp Marketing | 3+ tactics |
        | Digital Advertising | 3+ tactics |
        | PR & Media | 3+ tactics |

        4. Month-wise Channel & Activity Planner
        Purpose: Month-by-month execution directly derived from Core Strategies + informed by seasonality, cultural events, and ROI potential.

        Table format:
        | Month | Primary Channels | Key Activities | Expected Impact |

            • Select 2–4 primary channels each month based on demand spikes, seasonality, and local events.
            • List 3–5 specific, named campaigns or activities with hooks, formats, and audience focus.
            • Expected impact must be business-outcome focused (awareness lift %, leads, revenue uplift).

        5. Timeline Overview

        | Phase     | Key Activities |
        |-----------|----------------|
        | Months 1–3 | 3–5 activities |
        | Months 4–6 | 3–5 activities |
        | Months 7–9 | 3–5 activities |
        | Months 10–12 | 3–5 activities |

        6. Budget Estimate (Per Month)

        | Activity   | Estimated Cost (£) |
        |------------|--------------------|
        | [Activity] | £XXX               |
        | Total      | £X–£Y              |

        Budget must align with Perplexity benchmarks + user input.

        7. Key Metrics to Track

        | KPI | Measurement Method |
        |-----|--------------------|
        | [KPI] | [Method] |


        """
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_message},
        ]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        print("🟢 OpenAI generated plan successfully.")
        return content
    except Exception as e:
        print("❌ Error in call_openai_tool:", str(e))
        return None


def selected_strategy_expansion(business_info, perplexity_data, current_plan, user_message):

    business_name = business_info.get("business_name", "Unknown")
    business_type = business_info.get("business_type", "Unknown")
    location = business_info.get("location", "Unknown")
    website_link = business_info.get("website_link", "Unknown")
    business_goals = business_info.get("business_goals", "Unknown")
    marketing_budget = business_info.get("marketing_budget", "Unknown")
    target_audience = business_info.get("target_audience", "Unknown")
    current_marketing_assets = business_info.get("current_marketing_assets", "Unknown")
    brand_voice = business_info.get("brand_voice", "Unknown")

    research_context = json.dumps(perplexity_data, indent=2)

    system_message = f"""
        You are a **Marketing Strategy Refinement Assistant**.

        ### Context
        Business Name: {business_name}  
        Business Type: {business_type}  
        Location: {location}  
        Business Goals: {business_goals}  
        Brand Voice: {brand_voice}  
        Website: {website_link}  
        Marketing Budget: {marketing_budget}  
        Target Audience: {target_audience}  
        Current Marketing Assets: {current_marketing_assets}  

        ### Research Data (Perplexity):
        {research_context}

        ### Current Marketing Plan:
        {current_plan}

        ### User Message:
        {user_message}

        ---

        ### Task
        Your role is to assist the user in **refining and finalizing their marketing plan** through an interactive chat.  

        - Answer **clearly, concisely, and to the point** when handling questions.  
        - If the user requests **expansion, adjustment, or edits**, update the marketing plan accordingly.  
        - Always return the **full updated marketing plan** when modifications are requested (not just the changes).  
        - Maintain the **structure and formatting** of the plan (sections, strategies, timelines, action items, JSON if present).  
        - When the user says the plan is final, provide a **concise summary** of the final plan and explain the **reasons for the changes** made.  
        - Use all context (business info, research data, existing plan) to ensure consistency in recommendations.  

        Be professional, practical, and keep responses **solution-oriented**.
        """



    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_message},
        ]
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
