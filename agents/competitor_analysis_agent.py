from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv  

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def run_competitor_analysis(product: str, competitor_data: str) -> str:
    prompt = PromptTemplate.from_template("""
You are a market research analyst AI. Based on the following research data about competitors for the product "{product}", perform a detailed competitor analysis.

Competitor Research Data:
{competitor_data}

For the top 3 competitors mentioned, analyze and present the following for each:

1. SWOT Analysis  
2. Pricing Strategy (Freemium, subscription tiers, per-user, etc.)  
3. Value Proposition  
4. Client Types / Ideal Customer Profile (ICP)  
5. Positioning (How is the product positioned in the market)  
6. Marketing Strengths, including:  
   - Social media following  
   - Famous campaigns  
   - Collaborations with influencers/celebrities  
   - User-generated content (UGC) presence  
   - Product reviews (on G2, Capterra, ProductHunt for B2B; Amazon, Etsy, eBay for B2C)  

Present your output in a clear structured format with each competitor analyzed separately.

Respond only based on the provided data. If data is missing or unclear, indicate so transparently.
""")
    
    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run(product=product, competitor_data=competitor_data)
