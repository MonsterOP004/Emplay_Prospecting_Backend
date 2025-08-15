from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def customer_research_prompt(
    user_structured_input : str,
    previous_agent_output : str | None = None
) -> str:

    business_category = user_structured_input.get("business_category", "")
    geography = user_structured_input.get("geography", "")
    customer_trends = user_structured_input.get("customer_trends", "")
    behavioral_data = user_structured_input.get("behavioral_data", "")

    prompt = PromptTemplate.from_template("""
You are an expert in market segmentation and customer profiling.

Based on the internal and external information below, define the Ideal Customer Profile (ICP) for a small business.

Internal Business Details:
-Business Category: {business_category}
-Geography: {geography}
-Customer Trends: {customer_trends}
-Behavioral Data: {behavioral_data}

External Data:
{previous_agent_output}

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
        "business_category": business_category,
        "geography": geography,
        "customer_trends": customer_trends,
        "behavioral_data": behavioral_data,
    })
