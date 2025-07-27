# product_question_agent.py

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def clarify_product(product_idea: str) -> str:
    prompt = PromptTemplate.from_template("""
You're an AI assistant helping with market research. A user has input a brief description of a product or service: "{product_idea}".

Ask clarifying questions (in your mind) and generate a refined summary of:
- Product/Service Description
- Target Market
- Key Features
- Industry Context (if applicable)

Be concise and informative.

Respond only with the enhanced product description.
""")
    
    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run(product_idea=product_idea)
