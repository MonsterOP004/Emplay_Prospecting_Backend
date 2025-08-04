from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def competitor_research_prompt(product: str, description: str, pricing: str, sales_model: str, product_analysis: str) -> str:
    print("\n🌐 Searching for real-time business and market context using Tavily...\n")

    # Combine all available context to get better results from search
    search_query = f"""
Identify the business category, target geography, relevant keywords, and known competitors for the product: "{product}".
Description: {description}
Sales Model: {sales_model}
Pricing: {pricing}
Additional analysis: {product_analysis}
"""
    raw_web_data = search_web(search_query)
    summarized_context = summarize_long_text(raw_web_data,task="competitive landscape and business insights relevant to this product")

    prompt = PromptTemplate.from_template("""
Use the following context gathered from real-time search and product metadata to perform detailed competitor research:

Product: {product}
Description: {description}
Pricing: {pricing}
Sales Model: {sales_model}
Product Analysis: {product_analysis}

Search-Derived Context:
{competitor_research_landscape}

Conduct a detailed competitor research for businesses in the identified category and geography, with extracted keywords.

For the top 3–5 competitors (if available), include:

1. SWOT Analysis – Strengths, Weaknesses, Opportunities, and Threats
2. Pricing – Price points, bundling, discounting, premium vs budget positioning
3. Value Proposition – Taglines, promises, what benefits they highlight
4. Client Base – Demographics, geography, psychographics, behavioral traits
5. Positioning – Are they luxury or mass-market, niche or broad, aspirational or functional?
6. Marketing Strengths – Social media, campaigns, influencer/celebrity collabs
7. Review Strengths – Review platforms like Amazon, G2, Capterra, etc.
8. Competitive Positioning – Pricing, branding, and service comparisons
9. Channel Strategy – Instagram, TikTok, website, marketplaces, or physical stores

Structure each competitor’s insights under a heading with bullet points.
Avoid using a table.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    output = chain.run({
        "product": product,
        "description": description,
        "pricing": pricing,
        "sales_model": sales_model,
        "product_analysis": product_analysis,
        "competitor_research_landscape": summarized_context,
    })

    return output
