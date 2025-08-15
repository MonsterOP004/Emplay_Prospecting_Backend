from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def gtm_analysis_prompt(
    user_structured_input : str,
    previous_agent_output : str | None = None
    ) -> str:

    brand_presence = user_structured_input.get("brand_presence")
    icp = user_structured_input.get("icp")
    jtbd = user_structured_input.get("jtbd")
    content_performance = user_structured_input.get("content_performance")

    prompt = PromptTemplate.from_template("""
You are a GTM strategist for small and medium businesses. Based on the details provided, analyze and suggest a clear channel strategy plan.

Inputs:
- Brand presence: {brand_presence}
- ICP: {icp}
- JTBD: {jtbd}
- Content performance: {content_performance}

External Input:
- Previous agent output: {previous_agent_output}

What you should do:
1. Analyze current channels — including social media platforms, websites, listing directories, and offline presence (e.g., banners, word-of-mouth, in-store material).
2. Identify which of these channels are active vs inactive or underutilized.
3. Evaluate how well-optimized and engaging these channels are — frequency, quality of content, audience interaction.
4. Recommend 3–5 high-impact channels that fit the ICP and JTBD.
5. For each recommended channel, explain what kind of JTBD it can best support and how.

Output Format:
- Present the analysis in well-written paragraphs.
- Do not use tables or bullet points.
- Make the output practical, strategic, and grounded in SMB context.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({
        "brand_presence": brand_presence,
        "icp": icp,
        "jtbd": jtbd,
        "content_performance": content_performance,
    })
