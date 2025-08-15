from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def competitor_analysis_prompt(
  user_structured_input: str,
  previous_agent_output: str | None = None
) -> str:

    competitor_websites = user_structured_input.get("competitor_websites")
    review_sites = user_structured_input.get("review_sites")
    social_links = user_structured_input.get("social_links")
    
    search_query = f"competitor analysis for {competitor_websites} {review_sites} {social_links}"
    search_result = search_web(search_query)
    summarized_search = summarize_long_text(search_result,task="top competitors, their websites, socials, and product review insights") if search_result else "No external data found."

    # 🧠 Step 2: Prepare prompt
    prompt = PromptTemplate.from_template("""
You are a competitive intelligence analyst.

Using the internal and external data below, generate a competitor analysis.

Internal Data:
- Competitor Websites: {competitor_websites}
- Review Sites: {review_sites}
- Social Links: {social_links}

External Web Search Summary:
{competitor_analysis_landscape}

For each competitor (3–5 if possible), give insights in this format:

Competitor <Name>:
- SWOT:
  - Strengths:
  - Weaknesses:
  - Opportunities:
  - Threats:
- Pricing Strategy: Include pricing tiers, bundles, discount schemes
- Value Proposition: Brand tagline, value promise, core benefits
- Target Audience:
  - Demographics (age, gender, income, etc.):
  - Geographic (country, region, city type):
  - Psychographic (emotions, pain points, opinions, values):
  - Behavioral (usage pattern, buyer journey stage, loyalty):
- Positioning: Luxury/Mass, Niche/Broad, Aspirational/Functional, Brand Perception
- Marketing Strengths:
  - Socials (followers, engagement, UGC, campaigns, influencer tie-ups)
- Review Strengths: What people say on Amazon, Etsy, Website, G2, etc.
- Competitive Positioning: How do they compare on pricing, branding, and service
- Channel Usage: Are they active on Instagram, TikTok, Meta, Website, Storefronts?

Don't use tables. Make the output narrative and easy to scan in bullet format.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)

    # Step 3: Run the chain
    return chain.run({
      "competitor_websites": competitor_websites,
      "review_sites": review_sites,
      "social_links": social_links,
      "competitor_analysis_landscape": summarized_search
    })
