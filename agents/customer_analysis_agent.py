from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def customer_analysis_prompt(
    user_structured_input : str,
    previous_agent_output : str | None = None
) -> str:

    website_url = user_structured_input.get("website_url", "")
    social_profiles = user_structured_input.get("social_profiles", "")
    persona_deck = user_structured_input.get("persona_deck", "")
    customer_reviews = user_structured_input.get("customer_reviews", "")

    
    prompt = PromptTemplate.from_template("""
You are a customer research expert. Your job is to finalize the Ideal Customer Profile (ICP) and build rich buyer personas based on the following inputs:

Internal Inputs:
- Website URL: {website_url}
- Social Profiles: {social_profiles}
- Persona Deck: {persona_deck}
- Customer Reviews: {customer_reviews}

External Inputs:
- Previous agent output: {previous_agent_output}

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
        "website_url": website_url,
        "social_profiles": social_profiles,
        "persona_deck": persona_deck,
        "customer_reviews": customer_reviews,
    })
