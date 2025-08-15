from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import json
load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def product_research_prompt(user_structured_input: str, previous_agent_output: str | None = None) -> str:

    data = json.loads(user_structured_input)

    product = data.get("product_name", "")
    description = data.get("description", "")
    pricing_model = data.get("pricing_model", "")
    product_website = data.get("product_website", "")
    sales_channel = data.get("sales_channels", "")

    prompt = PromptTemplate.from_template("""
You are a market research assistant.

Your task is to understand a business’s product or service based on the following details:

Product/Service Name: {product}
Basic Description or Brochure/Website URL: {description}
Pricing Details: {pricing_model}
Product Website: {product_website}
Sales Model: {sales_channel}


Based on this information, generate the following:
1. A clear list of the **core product or service offerings**.
2. Categorize each item as:
   - Digital or Physical
   - One-time or Recurring
3. Highlight any **unique features, differentiators**, or reasons it may be easy or hard to access/use.
4. Present everything in a readable format.

Output format:
- Offerings:
  - Name:
  - Description:
  - Category: [Digital/Physical, One-time/Recurring]
- Key Differentiators:
  - [point form]
    """)

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({
        "product": product,
        "description": description,
        "pricing_model": pricing_model,
        "product_website": product_website,
        "sales_channel": sales_channel,
    })
