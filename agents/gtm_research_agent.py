from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def gtm_research_prompt(
    user_structured_input : str,
    previous_agent_output : str | None = None
) -> str:

    industry_type = user_structured_input.get("industry_type")
    benchmarks = user_structured_input.get("benchmarks")
    top_channels = user_structured_input.get("top_channels")
    content_types = user_structured_input.get("content_types")

    prompt = PromptTemplate.from_template("""
You are a Go-To-Market (GTM) strategy expert. Based on the information below, identify effective marketing channel strategies for small and medium businesses (SMBs) in this domain.

Inputs:
- Industry Type: {industry_type}
- Benchmarks: {benchmarks}
- Top Channels: {top_channels}
- Content Types: {content_types}

External Input:
- Previous Agent Output: {previous_agent_output}

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
        "industry_type": industry_type,
        "benchmarks": benchmarks,
        "top_channels": top_channels,
        "content_types": content_types,
    })
