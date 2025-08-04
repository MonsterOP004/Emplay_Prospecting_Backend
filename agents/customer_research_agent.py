from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def customer_research_prompt(
    product: str,
    description: str,
    pricing: str,
    sales_model: str,
    product_analysis: str,
    competitor_analysis: str
) -> str:
    # 🔍 Step 1: Use Tavily Search
    search_query = f"""
    What is the business category, location, customer type, and key services offered for a business like: 
    Product: {product}, Description: {description}
    """
    search_result = search_web(search_query)
    summarized_search = summarize_long_text(search_result, task="business category, location, customer type, and services") if search_result else "No external data found."

    # 📋 Step 2: Prompt Template
    prompt = PromptTemplate.from_template("""
You are an expert in market segmentation and customer profiling.

Based on the internal and external information below, define the Ideal Customer Profile (ICP) for a small business.

Internal Business Details:
- Product: {product}
- Description: {description}
- Pricing: {pricing}
- Sales Model: {sales_model}
- Product Analysis: {product_analysis}
- Competitor Analysis: {competitor_analysis}

External Web Search Summary:
{customer_research_landscape}

Your task:
1. Identify the type of business (e.g., bakery, boutique, spa, gym, florist, local service provider).
2. Understand the nature of the product or service — is it transactional (one-time), subscription-based, seasonal, functional, aspirational, emotional, etc.
3. Determine the industry fit and broader category classification.

Output Format:
ICP Definition:
– Segment:
– Target Audience:
– Needs/Challenges:

Write in clear, bullet-style or brief narrative format. Avoid using tables.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({
        "product": product,
        "description": description,
        "pricing": pricing,
        "sales_model": sales_model,
        "product_analysis": product_analysis,
        "competitor_analysis": competitor_analysis,
        "customer_research_landscape": summarized_search
    })
