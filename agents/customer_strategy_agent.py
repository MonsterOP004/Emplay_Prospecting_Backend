from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
from tools.summarizer_tool import summarize_long_text

load_dotenv(override=True)

groq_llm = ChatGroq(temperature=0.3, model="llama-3.3-70b-versatile")

def customer_strategy_prompt(
    product: str,
    description: str,
    sales_model: str,
    product_analysis: str,
    competitor_analysis: str,
    customer_research: str,
    customer_analysis: str,
) -> str:
    # Step 1: Search the web for business stage, pain points, and marketing data
    query = f"{product} business stage, pain points, marketing campaign examples, growth goals"
    search_results = search_web(query)
    summarized_data = summarize_long_text(search_results, task="business stage, pain points, and marketing history")

    # Step 2: Create a JTBD-focused prompt
    strategy_prompt = PromptTemplate.from_template("""
You are a customer success strategist. Based on the product data, analysis, and external insights, identify the core jobs-to-be-done (JTBD) that the business is trying to solve.

Inputs:
- Product: {product}
- Product Description: {description}
- Sales Model: {sales_model}
- Product Analysis: {product_analysis}
- Competitor Analysis: {competitor_analysis}
- Customer Research: {customer_research}
- Customer Analysis: {customer_analysis}
- External Market Context (includes business stage, pain points, and past marketing data): {customer_strategy_landscape}

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
        "product": product,
        "description": description,
        "sales_model": sales_model,
        "product_analysis": product_analysis,
        "competitor_analysis": competitor_analysis,
        "customer_research": customer_research,
        "customer_analysis": customer_analysis,
        "customer_strategy_landscape": summarized_data
    })
