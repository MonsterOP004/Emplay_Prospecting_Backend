from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.product_info_agent import clarify_product
from agents.competitor_research_agent import run_competitor_research
from agents.competitor_analysis_agent import run_competitor_analysis

class GraphState(TypedDict):
    product: str            
    refined_product: str   
    competitor_data: str
    analysis: str

def clarification_node(state: GraphState) -> dict:
    refined = clarify_product(state["product"])
    return {"refined_product": refined}

def research_node(state: GraphState) -> dict:
    data = run_competitor_research(state["refined_product"])
    return {"competitor_data": data}

def analysis_node(state: GraphState) -> dict:
    product = state["refined_product"]
    competitor_data = state["competitor_data"]
    result = run_competitor_analysis(product, competitor_data)
    return {"analysis": result}

graph = StateGraph(GraphState)
graph.add_node("clarification", RunnableLambda(clarification_node))
graph.add_node("research", RunnableLambda(research_node))
graph.add_node("analysis", RunnableLambda(analysis_node))

graph.set_entry_point("clarification")
graph.add_edge("clarification", "research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", END)

app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()

def competitor_graph(product_input: str) -> dict:
    return app.invoke({"product": product_input})

if __name__ == "__main__":
    product_input = input("Briefly describe your product or service: ")
    final_output = competitor_graph(product_input)
    
    print("\n Refined Product Description:\n")
    print(final_output["refined_product"])
    
    print("\n Final Competitor Analysis:\n")
    print(final_output["analysis"])