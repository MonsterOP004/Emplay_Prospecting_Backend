from langchain.prompts import PromptTemplate

product_research_prompt = PromptTemplate.from_template("""
You are a helpful assistant extracting required structured fields from the user input for product research.

Extract the following from the user input:
- product_name
- description (if mentioned)
- pricing_model (if available)
- product_website (if mentioned)
- sales_channels (if mentioned)

User input:
{user_input}

Respond as a JSON object:
{
  "product_name": "...",
  "description": "...",
  "pricing_model": "...",
  "product_website": "..."
  "sales_channels": "..."
}
""")


product_analysis_prompt = PromptTemplate.from_template("""
Extract the following information from the user input for analyzing a product:

- product_features (core attributes or functionalities)
- use_cases (how it is used by customers)
- user_reviews (if mentioned)

User input:
{user_input}

Output as JSON:
{
  "product_features": "...",
  "use_cases": "...",
  "user_reviews": "..."
}
""")


competitor_research_prompt = PromptTemplate.from_template("""
You are helping identify competitors. Extract the following from user input:

- product_category (e.g. fintech, SaaS, edtech)
- keywords (relevant search or market keywords)
- target_geography (e.g. India, US, Global)

User input:
{user_input}

Respond in JSON format:
{
  "product_category": "...",
  "keywords": "...",
  "target_geography": "..."
}
""")


competitor_analysis_prompt = PromptTemplate.from_template("""
Extract the following information from the user input for competitor analysis:

- competitor_websites (list of URLs)
- review_sites (e.g. G2, Trustpilot)
- social_links (social media URLs if available)

User input:
{user_input}

Output:
{
  "competitor_websites": [...],
  "review_sites": [...],
  "social_links": [...]
}
""")


customer_research_prompt = PromptTemplate.from_template("""
You are tasked with extracting customer research inputs.

Please extract:
- business_category
- geography (target region)
- customer_trends (from Google Trends or Analytics, if mentioned)
- behavioral_data (if mentioned like clickstream or funnel metrics)

User input:
{user_input}

Respond in this JSON format:
{
  "business_category": "...",
  "geography": "...",
  "customer_trends": "...",
  "behavioral_data": "..."
}
""")



customer_analysis_prompt = PromptTemplate.from_template("""
Extract the following fields for customer analysis:

- website_url
- social_profiles (LinkedIn, Twitter, Instagram, etc.)
- persona_deck (target customer persona slides if mentioned)
- customer_reviews (if mentioned)

User input:
{user_input}

Format output as:
{
  "website_url": "...",
  "social_profiles": [...],
  "persona_deck": "...",
  "customer_reviews": "..."
}
""")


customer_strategy_prompt = PromptTemplate.from_template("""
You are helping map out a customer’s strategic needs. Extract the following:

- business_goals
- business_stage (must be one of: early, growth, mature)
- marketing_problems (pain points they are facing)

User input:
{user_input}

Output:
{
  "business_goals": "...",
  "business_stage": "...",
  "marketing_problems": "..."
}
""")



gtm_research_prompt = PromptTemplate.from_template("""
Extract data for GTM (Go-To-Market) research.

Required fields:
- industry_type
- benchmarks (historical performance, if mentioned)
- top_channels (marketing channels used)
- content_types (content formats used)

User input:
{user_input}

Return in JSON:
{
  "industry_type": "...",
  "benchmarks": "...",
  "top_channels": [...],
  "content_types": [...]
}
""")



gtm_analysis_prompt = PromptTemplate.from_template("""
Extract the following GTM analysis fields:

- brand_presence (level of awareness, visibility, etc.)
- ICP (ideal customer profile characteristics)
- JTBD (Jobs-To-Be-Done insights)
- content_performance (metrics, if available)

User input:
{user_input}

Respond with:
{
  "brand_presence": "...",
  "ICP": "...",
  "JTBD": "...",
  "content_performance": "..."
}
""")


