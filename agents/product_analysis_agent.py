from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from tools.tavily_search import search_web
load_dotenv(override=True)
from tools.summarizer_tool import summarize_long_text
groq_llm = ChatGroq(temperature=0.3, model="llama-3.1-8b-instant")

def product_analysis_prompt(
    product : str,
    description : str,
    pricing : str,
    sales_model : str,
    product_research : str
) -> str:

    # Tavily searches
    features_info = search_web(f"Key features of {product} with description {description} and {pricing} and {sales_model}")
    reviews_info = search_web(f"Customer reviews of {product} with description {description} and {pricing} and {sales_model}")
    use_case_info = search_web(f"Use cases of {product} with description {description} and {pricing} and {sales_model}")

    summarized_features = summarize_long_text(features_info, "features")
    summarized_reviews = summarize_long_text(reviews_info, "customer review themes")
    summarized_use_cases = summarize_long_text(use_case_info, "use cases")

    prompt = PromptTemplate.from_template("""
You are a senior product analyst.

Below is a combination of direct inputs and web research on a product.

Use this data to generate product's analysis.

---

**Product Metadata**
- Product Name: {product}
- Description: {description}
- Pricing: {pricing}
- Sales Model: {sales_model}
- Internal Research (if any): {product_research}

**Web Research via Tavily**
- Features Info: {summarized_features}
- Customer Reviews: {summarized_reviews}
- Use Case Examples: {summarized_use_cases}

---

Please answer the following:

1. What are the top 3–5 **primary and secondary use cases** of this product?
2. How does this product create **value** in each use case? (Highlight user benefit and job-to-be-done.)
3. From the reviews, what are the most common:
   - **Positive patterns**
   - **Negative complaints**
4. Provide a **Feature vs Benefit Mapping** (List format; avoid tables for now)

Keep your tone analytical and objective. Do not make up features if missing.And keep your answers short and on point no extra explanation needed.
""")

    chain = LLMChain(llm=groq_llm, prompt=prompt)
    return chain.run({
        "product": product,
        "description": description,
        "pricing": pricing,
        "sales_model": sales_model,
        "product_research": product_research,
        "summarized_features": summarized_features,
        "summarized_reviews": summarized_reviews,
        "summarized_use_cases": summarized_use_cases
    })
