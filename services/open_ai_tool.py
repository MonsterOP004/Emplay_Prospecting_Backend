# openai_client.py
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ---------------------------
# Function 1: Generate Plan (Points 1-3)
# ---------------------------
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
    marketing_assets = business_info.get("current_marketing_assets", "Unknown")
    brand_voice = business_info.get("brand_voice", "Unknown")

    research_context = json.dumps(perplexity_data, indent=2)

    system_message = f"""
You are a senior marketing strategist and execution planner.

Your job is to synthesize **Perplexity research + user inputs** into:
- A 12-month strategic marketing plan  
- A Campaign Recommendation Table (summary selector for user choice)  

You must **never restate raw Perplexity data**; instead, interpret it into actionable decisions.  
Budgets, timelines, and tactics must reflect:  
- seasonality  
- buying triggers  
- competitor patterns  
- available assets  

---

### Inputs
Business Name: {business_name}  
Business Type: {business_type}  
Location: {location}  
Business Goals (12 months): {business_goals}  
Available Marketing Assets: {marketing_assets}  
Brand Voice & Tone: {brand_voice}  
Website: {website_link}  
Budget Range (approx., £): {marketing_budget}  
Perplexity Research Summary: {research_context}  

---

### Output Order

**1. Business & Brand Positioning**  
- Goal: 1–2 sentences aligned to research + user goals  
- Target Audience: 3–5 segments (descriptors, needs, triggers)  
- Brand Voice: 1 sentence  

**2. Marketing Objectives (12 months, SMART)**  
- Generate 3–5 SMART objectives (numeric targets + timeframes)  

**3. Campaign Recommendation Table (Summary Selector)**  
Each row = 1 recommended campaign, derived from objectives + research (seasonality, buying triggers, competitor gaps, assets, channel fit).  

Table Columns:  
| Objective | Audience | Key Message | Channel(s) | Timeline | Budget (£ est.) | KPI | Why This Now (Rationale) |  

- Populate 5–6 rows max (mix of always-on + seasonal/event-based)  
- “Why This Now” must explicitly cite **seasonality, buying triggers, or competitor gap**  
- Stay within {marketing_budget}  
- Keep scripts out — this table is only for selection  

---

### Guardrails
- Keep total costs inside {marketing_budget}  
- Respect brand voice & compliance  
- Use placeholders like {{FirstName}}, {{City}}, {{OfferEndDate}} where personalization applies  
- Consolidate overlapping ideas  
- For missing data → mark as **“estimated”**
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": system_message}],
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


# ---------------------------
# Function 2: Expand Strategy (Point 4)
# ---------------------------
def selected_strategy_expansion(business_info, perplexity_data, current_plan, user_message):
    business_name = business_info.get("business_name", "Unknown")
    business_type = business_info.get("business_type", "Unknown")
    location = business_info.get("location", "Unknown")
    website_link = business_info.get("website_link", "Unknown")
    business_goals = business_info.get("business_goals", "Unknown")
    marketing_budget = business_info.get("marketing_budget", "Unknown")
    current_marketing_assets = business_info.get("current_marketing_assets", "Unknown")
    brand_voice = business_info.get("brand_voice", "Unknown")

    research_context = json.dumps(perplexity_data, indent=2)

    system_message = f"""
You are a **Marketing Strategy Refinement Assistant**.  

The user will pick campaigns from the Recommendation Table.  
Your task is to expand into **Execution Briefs (Point 4)** for the chosen campaign(s).  

---

### Execution Briefs for Selected Campaigns

**A) Campaign Blueprint**  
- Campaign Name & Goal  
- Audience + Segments (with triggers, motivations, intent signals)  
- Message Pillars (3–5 core messages, with 1–2 sample lines each)  
- Channel-Specific Playbooks:  
  * Objectives & Funnel Role (awareness, nurture, conversion, retention)  
  * Formats (Reels, Carousels, Ads, Landing Pages, Emails, SMS, Calls, etc.)  
  * Cadence & Timeline → with exact posting/sending dates & frequency (e.g., “Day 1: Launch email, Day 3: Reel, Day 5: SMS reminder”)  
  * Targeting Details (personas, geo, lookalikes, retargeting rules)  
  * A/B Test Plan (hypothesis + what variable changes)  
  * KPI Plan (metrics, checkpoints, measurement frequency)  
  * Budget Allocation (per channel/asset)  
  * Strategist Rationale → 3–5 bullets referencing seasonality, triggers, competitor gaps, asset leverage  

**B) Content & Copy Starters (with CTAs)**  
- Ad Copy (3–5 headlines, 2–3 body texts, CTAs)  
- Social Posts: Reel script, captions, hashtags  
- Emails: subject lines, preheader, body outline, CTA, send cadence  
- SMS/WhatsApp: 3 variants, CTA, send timing notes  
- Landing Page/Web: Hero H1/H2, bullets, CTA, trust signals  
- Creative Direction: colors, imagery, motifs, aspect ratios  
👉 For every asset: include CTA + 1–2 sentence rationale  

**C) JSON Action Plan (Programmatic, per campaign)**  
{{
  "campaign_name": "Lead Nurture Email Sequence",
  "objective": "Convert free trial users to paid customers",
  "channels": [
    {{
      "name": "Email",
      "sequence": [
        {{"step": 1, "day": 0, "subject_line": "Welcome to [Product]", "body_copy": "Full email copy...", "cta": "Activate your account"}},
        {{"step": 2, "day": 3, "subject_line": "See how [Product] saves time", "body_copy": "Full email copy...", "cta": "Book a demo"}}
      ]
    }}
  ],
  "kpis": ["Open Rate", "CTR", "Conversion Rate"],
  "budget_estimate": "£2,000",
  "roles_needed": ["Copywriter", "Designer"],
  "success_criteria": "20% increase in conversions"
}}  

---

### Guardrails
- Keep total costs inside {marketing_budget}  
- Respect brand voice & compliance  
- Use placeholders like {{FirstName}}, {{City}}, {{OfferEndDate}}  
- Consolidate overlapping ideas  
- Missing data → mark as “estimated”  

User message: {user_message}  
Current Plan (context): {current_plan}  
Perplexity Research Summary: {research_context}  
"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": system_message}],
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
