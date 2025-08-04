from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def summarize_long_text(text: str, task: str) -> str:
    summarizer_prompt = PromptTemplate.from_template("""
You are a summarizer. Your task is to extract the key {task} from the following content:

Content:
{text}

Give a concise and informative bullet point summary.
""")
    chain = LLMChain(llm=groq_llm, prompt=summarizer_prompt)
    return chain.run({"text": text, "task": task})