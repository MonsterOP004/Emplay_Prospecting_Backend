# graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_core.runnables import Runnable
import sys
import os

# Ensure parent dir is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your agent prompt functions
from agents.product_research_agent import product_research_prompt
from agents.product_analysis_agent import product_analysis_prompt
from agents.competitor_research_agent import competitor_research_prompt
from agents.competitor_analysis_agent import competitor_analysis_prompt
from agents.customer_research_agent import customer_research_prompt
from agents.customer_analysis_agent import customer_analysis_prompt
from agents.customer_strategy_agent import customer_strategy_prompt
from agents.gtm_research_agent import gtm_research_prompt
from agents.gtm_analysis_agent import gtm_analysis_prompt
from agents.marketing_campaign_agent import marketing_campaign_prompt

# Import user input analyzer
from tools.llm_user_info_extractor import user_input_analyser

# Define playbook order
PLAYBOOK = [
    "Product Research",
    "Product Analysis",
    "Competitor Research",
    "Competitor Analysis",
    "Customer Research",
    "Customer Analysis",
    "Customer Strategy",
    "GTM Research",
    "GTM Analysis",
    "Marketing Campaign"
]

# Store pipeline state (could be replaced with Redis/DB for persistence)
pipeline_state = {
    "previous_agent_output": None
}

# Map agent names to their functions
AGENT_FUNCTIONS = {
    "Product Research": product_research_prompt,
    "Product Analysis": product_analysis_prompt,
    "Competitor Research": competitor_research_prompt,
    "Competitor Analysis": competitor_analysis_prompt,
    "Customer Research": customer_research_prompt,
    "Customer Analysis": customer_analysis_prompt,
    "Customer Strategy": customer_strategy_prompt,
    "GTM Research": gtm_research_prompt,
    "GTM Analysis": gtm_analysis_prompt,
    "Marketing Campaign": marketing_campaign_prompt
}

def run_single_agent(user_input: str, agent_name: str) -> str:

    if agent_name not in PLAYBOOK:
        raise ValueError(f"Invalid agent name '{agent_name}'.")

    agent_func = AGENT_FUNCTIONS[agent_name]

    user_structured_input = user_input_analyser(user_input, agent_name.lower().replace(" ", "_"))

    output = agent_func(user_structured_input, pipeline_state["previous_agent_output"])

    pipeline_state["previous_agent_output"] = output

    return output
