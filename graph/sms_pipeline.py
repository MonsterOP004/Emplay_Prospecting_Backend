from datetime import datetime, timedelta
import sys
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import atexit

# Load modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.ai_template_generator import sms_template_generator
from tools.csv_reader import load_audience
from tools.twilio_messenger import send_sms

# Set timezone to IST
IST = timezone("Asia/Kolkata")
scheduler = BackgroundScheduler(timezone=IST)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# --- Helpers ---

def load_custom_templates(filepath="templates/message_templates.json") -> dict:
    if not os.path.exists(filepath):
        print("❌ custom_templates.json not found.")
        return {}
    with open(filepath, "r") as file:
        return json.load(file)

def personalize_message(template: str, name: str, interest: str = None) -> str:
    return template.replace("{name}", name).replace("{interest}", interest or "")

def to_ist_timezone(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware in IST."""
    if dt.tzinfo is None:
        return IST.localize(dt)
    return dt.astimezone(IST)

def schedule_sms_send(message: str, phone: str, run_at: datetime):
    run_at = to_ist_timezone(run_at)
    job_id = f"sms_{phone}_{run_at.isoformat()}"
    scheduler.add_job(
        func=send_sms,
        trigger='date',
        run_date=run_at,
        args=[message, phone],
        id=job_id,
        replace_existing=True
    )
    print(f"🕓 Scheduled SMS to {phone} at {run_at.strftime('%Y-%m-%d %H:%M:%S %Z')} | Job ID: {job_id}")

# --- Main Program ---

def main():
    print("=== SMS Automation Agent ===\n")
    
    # 1. Get company and product info
    company = input("Enter your company name: ").strip()
    product = input("Enter your product/service name: ").strip()

    # 2. Choose template mode
    mode = input("Do you want to use (1) AI-generated or (2) Custom template? Enter 1 or 2: ").strip()

    # 3. Load audience CSV
    csv_path = input("Enter path to audience CSV file: ").strip()
    try:
        audience = load_audience(csv_path)
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return

    # 4. Template handling
    if mode == "1":
        print("🧠 Generating template using AI...")
        base_template = sms_template_generator(product)
    elif mode == "2":
        templates = load_custom_templates()
        if product not in templates:
            print(f"❌ No template found for product '{product}' in custom_templates.json.")
            return
        base_template = templates[product]
    else:
        print("❌ Invalid selection. Choose 1 or 2.")
        return

    print(f"\n📨 Base Template:\n{base_template}\n")

    # 5. Send or schedule messages
    for entry in audience:
        name = entry.get("name", "")
        phone = entry.get("phone", "")
        interest = entry.get("interest", "")

        message = personalize_message(base_template, name, interest)

        print(f"\n📱 Preparing SMS for {name} ({phone})")
        choice = input("Do you want to (1) Send now or (2) Schedule after 1 minute? Enter 1 or 2: ").strip()

        if choice == "1":
            try:
                sid = send_sms(message, phone)
                print(f"✅ Sent to {name} ({phone}) | SID: {sid}")
            except Exception as e:
                print(f"❌ Failed to send to {name} ({phone}): {e}")
        elif choice == "2":
            run_at = datetime.now() + timedelta(minutes=1)
            schedule_sms_send(message, phone, run_at)
        else:
            print("⚠️ Invalid choice. Skipping this entry.")

    print("\n✅ All messages processed. Scheduler will keep running for scheduled jobs.")

if __name__ == "__main__":
    main()
