from graph_1 import prospect_graph

def ask_product_details() -> None:
    print("\n🛍️  Enter Product/Service Details\n")

    product_name = input("1. Product/Service Name(s): ").strip()
    while not product_name:
        print("⚠️ Product/Service name cannot be empty.")
        product_name = input("1. Product/Service Name(s): ").strip()

    description_or_url = input("2. Basic Description or Brochure/Website URL (mandatory): ").strip()
    while not description_or_url:
        print("⚠️ Description or URL is required.")
        description_or_url = input("2. Basic Description or Brochure/Website URL (mandatory): ").strip()

    pricing = input("3. Pricing Details (if available, else press Enter to skip): ").strip()

    print("\n4. Select Sales Model:")
    print("   a) In-store")
    print("   b) Online")
    print("   c) Subscription")
    print("   d) One-time")
    print("   e) Other (you can describe)")

    valid_options = {
        "a": "In-store",
        "b": "Online",
        "c": "Subscription",
        "d": "One-time",
        "e": "Other"
    }

    sales_model_input = input("Choose a, b, c, d, or e: ").strip().lower()
    while sales_model_input not in valid_options:
        print("⚠️ Invalid option. Please choose a valid option (a–e).")
        sales_model_input = input("Choose a, b, c, d, or e: ").strip().lower()

    if sales_model_input == "e":
        sales_model = input("Describe your sales model: ").strip()
    else:
        sales_model = valid_options[sales_model_input]

    input_data = {
        "product": product_name,
        "description": description_or_url,
        "pricing": pricing,
        "sales_model": sales_model
    }

    print("\n🔍 Running AI analysis...\n")
    final_output = prospect_graph(input_data)

    print("\n✅ Customer Strategy:\n")
    print(final_output.get("customer_strategy", "Not available"))

    print("\n📊 Competitor Research:\n")
    print(final_output.get("competitor_research", "Not available"))

    # print("\n📊 Competitor Research:\n")
    # print(final_output.get("competitor_data", "Not available"))

    # print("\n📈 Final Competitor Analysis:\n")
    # print(final_output.get("analysis", "Not available"))


if __name__ == "__main__":
    ask_product_details()