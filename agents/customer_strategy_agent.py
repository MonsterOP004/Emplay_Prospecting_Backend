from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.3-70b-versatile")

def customer_strategy_prompt(
    user_structured_input : str,
    previous_agent_output : str | None = None
) -> str:
    
    business_goals = user_structured_input.get("business_goals")
    business_stage = user_structured_input.get("business_stage")
    marketing_problems = user_structured_input.get("marketing_problems") 

    # Step 2: Create a JTBD-focused prompt
    strategy_prompt = PromptTemplate.from_template("""
You are a customer success strategist. Based on the product data, analysis, and external insights, identify the core jobs-to-be-done (JTBD) that the business is trying to solve.

Inputs:
- Business Goals: {business_goals}
- Business Stage: {business_stage}
- Marketing Problems: {marketing_problems}

- External Market Context: {previous_agent_output}

Your task:
1. Identify **functional JTBDs** (e.g., “Get more walk-ins,” “Book more appointments,” “Sell old stock”).
2. Identify **emotional JTBDs** (e.g., “Look professional,” “Feel in control,” “Be seen as trendy”).
3. Map each JTBD to the appropriate **business stage** — early (acquisition), growth (retention or expansion), or mature (diversification).
4. Identify possible **triggers** for each JTBD — such as seasonality, local events, launches, or competitor activity.

Output Format:
- Provide a clear narrative listing JTBDs with relevant context.
- Mention how each JTBD aligns with the business stage.
- Include any identified triggers for each job.

Avoid tables. Use structured paragraphs in natural tone.
""")

    chain = LLMChain(llm=groq_llm, prompt=strategy_prompt)
    return chain.run({
        "business_goals": business_goals,
        "business_stage": business_stage,
        "marketing_problems": marketing_problems,
    })
