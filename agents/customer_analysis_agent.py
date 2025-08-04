from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def customer_analysis_prompt(
    product: str,
    description: str,
    sales_model: str,
    product_analysis: str,
    competitor_analysis: str,
    customer_research: str
) -> str:
    # 1. Perform Tavily Search for customer-related data
    search_query = f"Customer demographics, psychographics, website, social links, CRM data for {product} {description} {sales_model}"
    search_results = search_web(search_query)

    # 2. Summarize long results to extract usable input
    customer_insights = summarize_long_text(search_results, "demographics, psychographics, and web behavior for customer profiling")

    # 3. Prompt
    prompt = PromptTemplate.from_template("""
You are a customer research expert. Your job is to finalize the Ideal Customer Profile (ICP) and build rich buyer personas based on the following inputs:

- Product: {product}
- Description: {description}
- Sales Model: {sales_model}
- Product Analysis: {product_analysis}
- Competitor Analysis: {competitor_analysis}
- Customer Research Summary: {customer_research}
- Web & CRM Insights: {customer_analytics_landscape}

Tasks:
1. Map out customer demographic details (age, gender, income), geographic traits (urban/rural, tier 1/2/3 cities), and psychographics (values, behavior, decision drivers).
2. Identify core customer needs, pain points, and motivations.
3. Build 1–2 Ideal Customer Profiles (ICPs).
4. Create 1–2 complete Buyer Personas with the following attributes:
    - Name
    - Demographics (Age, Gender, Income, Location)
    - Profession
    - Web Behavior
    - Purchase History (if inferred)
    - Social Media Following or Influence
    - Pain Points
    - Buying Triggers
    - Preferred Communication Channels
    - Trusted Influencers

Ensure the output:
- Does not include tables.
- Is structured cleanly in paragraph or bullet format.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)

    return chain.run({
        "product": product,
        "description": description,
        "sales_model": sales_model,
        "product_analysis": product_analysis,
        "competitor_analysis": competitor_analysis,
        "customer_research": customer_research,
        "customer_analytics_landscape": customer_insights,
    })
