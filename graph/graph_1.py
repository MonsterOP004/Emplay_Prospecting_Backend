from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.product_analysis_agent import product_analysis_prompt
from agents.product_research_agent import product_research_prompt
from agents.competitor_research_agent import competitor_research_prompt
from agents.competitor_analysis_agent import competitor_analysis_prompt
from agents.customer_analysis_agent import customer_analysis_prompt
from agents.customer_research_agent import customer_research_prompt
from agents.customer_strategy_agent import customer_strategy_prompt
from agents.gtm_analysis_agent import gtm_analysis_prompt
from agents.gtm_research_agent import gtm_research_prompt


class GraphState(TypedDict):
    product: str
    description: str
    pricing: str
    sales_model: str
    product_research: str
    product_analysis: str
    competitor_research_data: str
    competitor_analysis: str
    customer_research: str
    customer_analysis: str
    customer_strategy: str
    gtm_research: str
    gtm_analysis: str


# ----------------- Nodes -----------------

def product_research_node(state: GraphState) -> dict:
    product_research_results = product_research_prompt(
        product=state["product"],
        description=state.get("description", ""),
        pricing=state.get("pricing", ""),
        sales_model=state.get("sales_model", "")
    )
    return {"product_research": product_research_results}

def product_analysis_node(state: GraphState) -> dict:
    refined = product_analysis_prompt(
        product=state["product"],
        description=state.get("description", ""),
        pricing=state.get("pricing", ""),
        sales_model=state.get("sales_model", ""),
        product_research=state.get("product_research", "")
    )
    return {"product_analysis": refined}

def competitor_research_node(state: GraphState) -> dict:
    data = competitor_research_prompt(
        product=state["product"],
        description=state.get("description", ""),
        pricing=state.get("pricing", ""),
        sales_model=state.get("sales_model", ""),
        product_analysis = state["product_analysis"])
    return {"competitor_research_data": data}

def competitor_analysis_node(state: GraphState) -> dict:
    result = competitor_analysis_prompt(
        product=state["product"],
        description=state.get("description", ""),
        product_analysis=state["product_analysis"],
        competitor_research_data=state["competitor_research_data"]
    )
    return {"competitor_analysis": result}

def customer_research_node(state: GraphState) -> dict:
    result = customer_research_prompt(
        product=state["product"],
        description=state.get("description", ""),
        pricing=state.get("pricing", ""),
        sales_model=state.get("sales_model", ""),
        product_analysis=state["product_analysis"],
        competitor_analysis=state["competitor_analysis"])
    return {"customer_research": result}

def customer_analysis_node(state: GraphState) -> dict:
    result = customer_analysis_prompt(
        product=state["product"],
        description=state.get("description", ""),
        sales_model=state.get("sales_model", ""),
        product_analysis=state["product_analysis"],
        competitor_analysis=state["competitor_analysis"],
        customer_research=state["customer_research"]
    )
    return {"customer_analysis": result}

def customer_strategy_node(state: GraphState) -> dict:
    result = customer_strategy_prompt(
        product=state["product"],
        description=state.get("description", ""),
        sales_model=state.get("sales_model", ""),
        product_analysis=state["product_analysis"],
        competitor_analysis=state["competitor_analysis"],
        customer_research=state["customer_research"],
        customer_analysis=state["customer_analysis"]
    )
    return {"customer_strategy": result}

def gtm_research_node(state: GraphState) -> dict:
    result = gtm_research_prompt(
        industry_data=state["product_analysis"],
        competitor_research_data=state["competitor_research_data"]
    )
    return {"gtm_research": result}

def gtm_analysis_node(state: GraphState) -> dict:
    result = gtm_analysis_prompt(
        brand_presence="Based on customer strategy: " + state["customer_strategy"],
        icp_jtbd=state["customer_analysis"],
        content_insights=state["gtm_research"]
    )
    return {"gtm_analysis": result}


# ----------------- Graph Definition -----------------

graph = StateGraph(GraphState)

graph.add_node("product_research", RunnableLambda(product_research_node))
graph.add_node("product_analysis", RunnableLambda(product_analysis_node))
graph.add_node("competitor_research", RunnableLambda(competitor_research_node))
graph.add_node("competitor_analysis", RunnableLambda(competitor_analysis_node))
graph.add_node("customer_research", RunnableLambda(customer_research_node))
graph.add_node("customer_analysis", RunnableLambda(customer_analysis_node))
graph.add_node("customer_strategy", RunnableLambda(customer_strategy_node))
graph.add_node("gtm_research", RunnableLambda(gtm_research_node))
graph.add_node("gtm_analysis", RunnableLambda(gtm_analysis_node))

# Entry and transitions
graph.set_entry_point("product_research")
graph.add_edge("product_research", "product_analysis")
graph.add_edge("product_analysis", "competitor_research")
graph.add_edge("competitor_research", "competitor_analysis")
graph.add_edge("competitor_analysis", "customer_research")
graph.add_edge("customer_research", "customer_analysis")
graph.add_edge("customer_analysis", "customer_strategy")
graph.add_edge("customer_strategy", END)
# graph.add_edge("customer_strategy", "gtm_research")
# graph.add_edge("gtm_research", "gtm_analysis")
# graph.add_edge("gtm_analysis", END)

# Compile the graph
app = graph.compile()

# Optional: visualize the graph
print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()


def prospect_graph(product_input: str, desc="", pricing="", sales="") -> dict:
    return app.invoke({
        "product": product_input,
        "description": desc,
        "pricing": pricing,
        "sales_model": sales
    })


# if __name__ == "__main__":

#     product_input = input("Briefly describe your product or service name: ")
#     description = input("Short description or website/brochure URL: ")
#     pricing = input("Pricing details (optional): ")
#     sales_model = input("Sales model (online, subscription, etc.): ")

#     final_output = prospect_graph(product_input, description, pricing, sales_model)

#     print("\n--- Refined Product Description ---\n")
#     print(final_output["product_analysis"])

#     print("\n--- Competitor Analysis ---\n")
#     print(final_output["competitor_analysis"])

#     print("\n--- Customer Strategy ---\n")
#     print(final_output["customer_strategy"])

#     print("\n--- GTM Channel Strategy ---\n")
#     print(final_output["gtm_analysis"])
