from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def product_research_prompt(product: str, description: str, pricing: str, sales_model: str) -> str:
    prompt = PromptTemplate.from_template("""
You are a market research assistant.

Your task is to understand a business’s product or service based on the following details:

Product/Service Name: {product}
Basic Description or Brochure/Website URL: {description}
Pricing Details: {pricing}
Sales Model: {sales_model}

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
        "pricing": pricing,
        "sales_model": sales_model
    })
