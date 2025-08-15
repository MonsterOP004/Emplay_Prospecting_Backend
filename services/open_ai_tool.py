# openai_client.py
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def call_openai_tool(form_data, perplexity_data):

    business_name = form_data.get("business_name", "Unknown")
    business_type = form_data.get("business_type", "Unknown")
    location = form_data.get("location", "Unknown")
    website_link = form_data.get("website_link", "Unknown")
    business_goals = form_data.get("business_goals", "Unknown")
    marketing_budget = form_data.get("marketing_budget", "Unknown")

    research_context = json.dumps(perplexity_data, indent=2)

    system_message = """
12-Month Marketing Plan with Execution Pathway (Perplexity-Optimized)

Create a detailed 12-month marketing plan for the following business:

Business Name: {business_name}
Business Type: {business_type}
Location: {location}
Business Goals: {business_goals}
Available Marketing Assets: {marketing_assets}
Brand Voice: {brand_voice}
Website: {website_link}
Marketing Budget: {marketing_budget}

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

8. Action Items Dictionary (Clickable Plan)
Produce a JSON-like object containing all tactical actions from Core Strategies + Month-wise Planner:

{
    "plan_id": "unique_id",
    "preferences": {
        "budget_range": "£X–£Y",
        "primary_objectives": ["Objective 1", "Objective 2"],
        "brand_voice": "{brand_voice}"
    },
    "action_items": [
        {
            "month": 1,
            "channel": "Instagram",
            "campaign": "New Arrival Launch",
            "tasks": [
                "Create teaser reel",
                "Post customer testimonial carousel",
                "Run 5-day story countdown"
            ],
            "estimated_cost": "£XXX",
            "expected_impact": "Awareness +15%"
        }
    ]
}

Post-Selection Execution Expansion Prompt
Input:
    • selected_strategy_ids
    • month_activity_selections (optional)
    • budget_range_gbp
    • brand_voice
    • marketing_assets

Task:
Expand only the selected strategies into execution-ready blueprints + programmatic JSON action list.
For each selected strategy:
    • Campaign Blueprint: Campaign name, goal, audience targeting, messaging pillars, formats, cadence, seasonality hooks, KPIs, and budget allocation.
    • Content & Copy Starters: Subject lines, captions, CTAs, outlines.
    • Action Items Dictionary: JSON schema with atomic tasks, assets needed, owner role, due dates, estimated cost, and expected impact.
"""

def selected_strategy_expansion(form_data, perplexity_data, selection):

    business_name = form_data.get("business_name", "Unknown")
    business_type = form_data.get("business_type", "Unknown")
    location = form_data.get("location", "Unknown")
    website_link = form_data.get("website_link", "Unknown")
    business_goals = form_data.get("business_goals", "Unknown")
    marketing_budget = form_data.get("marketing_budget", "Unknown")

    research_context = json.dumps(perplexity_data, indent=2)
    user_selected_data = json.dumps(selection.get("selected_strategy_ids", []), indent=2)
    month_activity_selections = json.dumps(selection.get("month_activity_selections", []), indent=2)


    system_message = """
12-Month Marketing Plan with Execution Pathway (Perplexity-Optimized)

Create a detailed 12-month marketing plan for the following business:

Business Name: {business_name}
Business Type: {business_type}
Location: {location}
Business Goals: {business_goals}
Available Marketing Assets: {marketing_assets}
Brand Voice: {brand_voice}
Website: {website_link}
Marketing Budget: {marketing_budget}

Perplexity Research Data:
{research_context}

User Selected Data:
{user_selected_data}

Month Activity Selections:
{month_activity_selections}

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


Task:
Expand only the selected strategies into execution-ready blueprints + programmatic JSON action list.
For each selected strategy:
    • Campaign Blueprint: Campaign name, goal, audience targeting, messaging pillars, formats, cadence, seasonality hooks, KPIs, and budget allocation.
    • Content & Copy Starters: Subject lines, captions, CTAs, outlines.
    • Action Items Dictionary: JSON schema with atomic tasks, assets needed, owner role, due dates, estimated cost, and expected impact.
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
