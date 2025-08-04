from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def gtm_research_prompt(industry: str, current_channels: str, competitor_tactics: str) -> str:
    prompt = PromptTemplate.from_template("""
You are a Go-To-Market (GTM) strategy expert. Based on the information below, identify effective marketing channel strategies for small and medium businesses (SMBs) in this domain.

Inputs:
- Business Industry: {industry}
- Existing Marketing Channel Presence: {current_channels}
- Competitor Marketing Tactics (if known): {competitor_tactics}

What to do:
1. Identify the top 3–5 most effective marketing channels for SMBs in this industry — e.g., Instagram, WhatsApp, Google Business, in-store offers, referral programs, Snapchat, Twitter, LinkedIn, etc.
2. Specify which channels are **seasonal** (e.g., used during holidays or peak times) vs **always-on**.
3. Describe what **types of content** work best on these channels — e.g., reels, testimonial videos, before/after photos, direct messages (DMs), SMS, stories, or simple social posts.
4. Mention the **messaging tone** typically used — formal/informal, personal, humorous, urgent, etc.
5. Provide examples or insights based on what has worked well for similar competitors or local players.

Output Format:
- Write in clear, flowing paragraphs.
- Avoid using bullet points or tables.
- Focus on practical insights and actionable observations.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({
        "industry": industry,
        "current_channels": current_channels,
        "competitor_tactics": competitor_tactics
    })
