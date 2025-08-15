# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perplexity_tool import perplexity_tool_prompt, call_perplexity
from open_ai_tool import call_openai

def extract_perplexity_sections(perplexity_text):
   
    sections = {
        "company_research": None,
        "competitor_research": None,
        "sales_benchmarks": None,
        "best_channels": None
    }

    text_lower = perplexity_text.lower()
    if "company research" in text_lower:
        sections["company_research"] = perplexity_text
    if "competitor" in text_lower:
        sections["competitor_research"] = perplexity_text
    if "sales benchmarks" in text_lower:
        sections["sales_benchmarks"] = perplexity_text
    if "best channels" in text_lower:
        sections["best_channels"] = perplexity_text

    return sections


def generate_marketing_plan(form_data):

    perplexity_prompt = build_perplexity_prompt(form_data["website_link"])
    perplexity_result = call_perplexity(perplexity_prompt)

    sections = extract_perplexity_sections(perplexity_result)

    openai_result = call_openai(form_data, sections)

    return {
        "marketing_plan": openai_result
    }

if __name__ == "__main__":
    form_data = {
        "business_name": "Willow and Rose Makeup",
        "business_type": "Professional Makeup Studio",
        "location": "Surrey, UK",
        "website_link": "https://www.willowandrosemakeup.co.uk/about",
        "business_goals": "Increase sales by 20%, increase Instagram followers by 5000, Improve website traffic by 20%",
        "marketing_assets": "Social Media Channels",
        "brand_voice": "Professional, Creative, and Innovative"
    }

    output = generate_marketing_plan(form_data)
    print("\n=== MARKETING PLAN ===\n")
    print(output["marketing_plan"])