from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def marketing_campaign_prompt(
   previous_agent_output: str
) -> str:

    prompt = PromptTemplate.from_template("""
You are an expert in marketing strategy execution planning.

Input : 
{previous_agent_output}

Your task:  
Build a detailed execution roadmap for the provided business/product context.  

Steps to follow:  
1. Combine ICP (Ideal Customer Profile) + JTBD (Jobs To Be Done) + preferred marketing channels.  
2. Write **core message pillars**: value proposition, main customer pains, proof points.  
3. Build a **content calendar**: weekly posts, email cadence, blog frequency.  
4. Define **Inbound strategy**: SEO, blogs, lead magnets, communities, social media.  
5. Define **Outbound strategy**: cold email, LinkedIn DMs, WhatsApp drips, retargeting ads.  
6. Build a **PESO plan**:  
   - Paid (ads)  
   - Earned (press, collaborations)  
   - Shared (social media engagement)  
   - Owned (website, email lists)  
7. Include a **sample CTA bank**.  
8. Define **success metrics**: soft (reach, views) and hard (leads, conversions).  

Output Format:  
- **1-page strategy** (narrative or bullet points, no tables)  
- **Messaging themes** (grouped by value/pain/proof)  
- **Weekly, Monthly, Quarterly Marketing Calendar** (30/60/90 days)  
- **Inbound & Outbound tactics** clearly separated  
- **PESO framework** section  

Write in clear, bullet-style or brief narrative format. Avoid using tables.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({
        "previous_agent_output": previous_agent_output
    })
