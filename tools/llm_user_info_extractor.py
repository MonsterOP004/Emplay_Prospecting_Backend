from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.user_info_prompts import (
    product_research_prompt,
    product_analysis_prompt,
    competitor_research_prompt,
    competitor_analysis_prompt,
    customer_research_prompt,
    customer_analysis_prompt,
    customer_strategy_prompt,
    gtm_research_prompt,
    gtm_analysis_prompt
)

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

PROMPT_MAP = {
    "product_research": product_research_prompt,
    "product_analysis": product_analysis_prompt,
    "competitor_research": competitor_research_prompt,
    "competitor_analysis": competitor_analysis_prompt,
    "customer_research": customer_research_prompt,
    "customer_analysis": customer_analysis_prompt,
    "customer_strategy": customer_strategy_prompt,
    "gtm_research": gtm_research_prompt,
    "gtm_analysis": gtm_analysis_prompt
}

def user_input_analyser(user_input: str, agent_name: str) -> dict:
    
    prompt = PROMPT_MAP.get(agent_name)
    if not prompt:
        raise ValueError("Invalid agent name provided.")
    
    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({"user_input": user_input, agent_name: agent_name})

