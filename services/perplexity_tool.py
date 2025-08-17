# perplexity.py
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def perplexity_tool_prompt(website_link):
    return f"""
      1. Company Research
  Use the provided business website: {website_link}
  Analyze the website to understand products/services, positioning, and unique selling points.
  Use credible and up-to-date sources (news and review sites) to assess:

  Target customers & audience segments
  Market presence & local/national reputation
  Online presence & visibility (SEO strengths, review ratings, notable citations/mentions)
  Notable recent developments or launches (include dates)
  Scan publicly available social media profiles connected to the business (Instagram, Facebook, X, TikTok, LinkedIn, Pinterest, YouTube). 

  For each:

  Platform name & URL
  Follower count (if visible)
  Posting frequency & consistency (e.g., avg posts/week)
  2–3 recent post examples with links (prefer last 60–90 days)
  Observed engagement style (low / medium / high; include typical likes/comments only if clearly visible)
  Common content themes and tone
  Visible collaborations/influencer work/promotions (evidence)
  Notable creative patterns (e.g., reels, carousels, educational posts, product shots)

  Note: Focus on qualitative insights that inform strategy. Only include quantitative metrics you can verify; if unavailable, provide best-available ranges and label as estimate. Always include source links and indicate data recency.
  
  2. Competitor Research
  Identify 3–5 direct competitors (local/regional/online alternatives) relevant to the business inferred from {website_link}.
  Provide in a Markdown table:
  Name & website
  Value proposition & differentiators
  Product/service range
  Pricing style (premium, mid-market, budget, subscription)
  Primary marketing channels used
  Notable campaigns/strategies worth learning from
  Sources (links)

  3. Sales Benchmarks
  Estimate sales performance for similar-sized businesses in this industry, both locally and nationwide in comparable cities.
  Provide:
  Annual revenue range
  Monthly sales range
  Average transaction value
  Seasonality patterns or sales spikes (by month/quarter)
  Cite credible industry sources. Where exact figures are unavailable, provide well-reasoned ranges and note the basis (e.g., industry reports, trade associations, benchmark studies).
  
  4. Best Channels & Themes
  Recommend the 3–5 most effective marketing channels for this type of business (as inferred from {website_link}), based on:
  Industry best practices
  Competitor performance patterns
  Audience behaviour and preferences surfaced above
  For each channel, include:
  Rationale and expected funnel role (Awareness / Consideration / Conversion / Retention)
  Primary KPIs to track
  2–3 proven content themes & formats (e.g., tutorials, testimonials, before/after, seasonal promos), with example links where possible
  Support recommendations with concise reasoning and examples; include sources for any external references.

  5. Customer Triggers & Buying Motivations
  Identify common buying triggers in this industry (e.g., price sensitivity, product upgrades, gifting, seasonal demand).
  Describe decision-making factors: convenience, prestige, urgency, discounts, social proof.
  Highlight typical objections/barriers to purchase and how competitors address them.

  6. Seasonal & Event Opportunities
  List relevant seasonal peaks, cultural/festival moments, and industry-specific events that drive sales (e.g., Mother’s Day, Black Friday, trade expos).
  Indicate timing (months/quarters).
  Suggest typical campaign themes tied to these events.
  Include competitor or industry examples with links where possible.

  Return output in **valid JSON** matching this schema exactly: 

  {{
    "company_research": {{
      "products_services": "",
      "positioning": "",
      "unique_selling_points": "",
      "target_customers": "",
      "market_presence": "",
      "online_presence": "",
      "recent_developments": "",
      "social_media_profiles": [
        {{
          "platform_name": "",
          "profile_url": "",
          "follower_count": "",
          "posting_frequency": "",
          "recent_posts": [
            {{"title": "", "link": ""}}
          ],
          "engagement_style": "",
          "content_themes": "",
          "collaborations": "",
          "creative_patterns": ""
        }}
      ]
    }},
    "competitor_research": [
      {{
        "name": "",
        "website": "",
        "value_proposition": "",
        "differentiators": "",
        "product_service_range": "",
        "pricing_style": "",
        "primary_channels": "",
        "notable_campaigns": ""
      }}
    ],
    "sales_benchmarks": {{
      "annual_revenue_range": "",
      "monthly_sales_range": "",
      "avg_transaction_value": "",
      "seasonality_patterns": ""
    }},
    "best_channels": [
      {{
        "channel": "",
        "rationale": "",
        "funnel_role": "",
        "primary_kpis": "",
        "proven_themes_formats": [""]
      }}
    ],
    "customer_triggers": {{
      "buying_triggers": "",
      "decision_factors": "",
      "objections_barriers": "",
      "competitor_responses": ""
    }},
    "seasonal_opportunities": [
      {{
        "event_name": "",
        "timing": "",
        "campaign_themes": "",
        "examples": ""
      }}
    ]
  }}

  Rules:
  - If data is not available or you are not able to find anything concrete then set the value to **null** in place of string acceptance or **an empty list** in place of list acceptance.
  - Keep responses concise but factual, with source links where possible.
  - Do not include extra text outside JSON.
  - Do not start with ``` json and end with ```. 
    """


def call_perplexity_tool(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def test_perplexity_tool():
    """Test function for perplexity_tool"""
    test_website = "https://www.willowandrosemakeup.co.uk/about"
    prompt = perplexity_tool_prompt(test_website)
    try:
        response = call_perplexity_tool(prompt)
        print(f"Perplexity API response: {response}")
        return True
    except Exception as e:
        print(f"Error calling perplexity tool: {e}")
        return False

if __name__ == "__main__":
    test_perplexity_tool()
