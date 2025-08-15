from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def competitor_research_prompt(
    user_structured_input: str,
    previous_agent_output: str | None = None,
) -> str:
    print("\n🌐 Searching for real-time business and market context using Tavily...\n")

    product_category = user_structured_input.get("product_category")
    keywords = user_structured_input.get("keywords")
    target_geography = user_structured_input.get("target_geography")

    search_query = f"Top competitors for {product_category} or similar products/services in {target_geography}. Include websites, social media links, and reviews."
    search_result = search_web(search_query)

    summarized_context = summarize_long_text(search_result)

    prompt = PromptTemplate.from_template("""
Use the following context gathered from real-time search and product metadata to perform detailed competitor research:

{competitor_research_landscape}

product_category: {product_category}
keywords: {keywords}
target_geography: {target_geography}

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
        "product_category": product_category,
        "keywords": keywords,
        "target_geography": target_geography,
        "competitor_research_landscape": summarized_context,
    })

    return output
