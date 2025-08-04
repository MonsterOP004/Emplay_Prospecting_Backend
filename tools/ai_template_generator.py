from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def sms_template_generator(product: str) -> str:
    prompt = PromptTemplate.from_template(
        """You are an expert SMS marketing copywriter. Write a short and catchy SMS template to promote the following product or service:

Product/Service: {product}

Make sure the message:
- Sounds personalized using the user's name: {name}
- Is under 160 characters
- Contains a clear call-to-action and optionally a discount code
- Does not sound robotic

Respond only with the template, no extra text."""
    )

    chain = prompt | groq_llm
    result = chain.invoke({"product": product, "name": "{name}"})  # Keep {name} placeholder
    return result.content  # ✅ Extract the actual string from AIMessage
