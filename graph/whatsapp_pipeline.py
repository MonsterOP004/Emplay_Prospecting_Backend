import os
import sys
from datetime import datetime
from dateutil import parser
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from io import StringIO
import csv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.csv_reader import load_audience
from tools.twilio_messenger import send_whatsapp  
# Initialize scheduler once for the whole app
IST = pytz.timezone("Asia/Kolkata")
scheduler = BackgroundScheduler(timezone=IST)
scheduler.start()


def send_bulk_whatsapp(message_text, sender_number, audience_data):
    """
    Send WhatsApp messages to a list of recipients.
    :param message_text: The message content
    :param sender_number: Twilio WhatsApp sender number (e.g. whatsapp:+14155238886)
    :param audience_data: List[dict] with 'name' and 'phone' keys
    """
    print(f"\n📨 Sending WhatsApp from {sender_number}:\n{message_text}\n")

    for entry in audience_data:
        name = entry.get("name", "")
        phone = entry.get("phone", "")
        try:
            sid = send_whatsapp(message_text, phone, from_number=sender_number)
            print(f"✅ Sent to {name} ({phone}) | SID: {sid}")
        except Exception as e:
            print(f"❌ Failed to send to {name} ({phone}): {e}")

    print("\n✅ All WhatsApp messages sent.")


def parse_csv_content(csv_bytes):
    """
    Parse CSV bytes into a list of dictionaries with 'name' and 'phone'.
    """
    try:
        text_data = csv_bytes.decode("utf-8")
        reader = csv.DictReader(StringIO(text_data))
        audience = []
        for row in reader:
            audience.append({
                "name": row.get("name", "").strip(),
                "phone": row.get("phone", "").strip()
            })
        return audience
    except Exception as e:
        raise ValueError(f"Failed to parse CSV: {e}")


def main(message_text, sender_number, csv_bytes, sending_period="instant", scheduled_time=None):
    """
    WhatsApp bulk messaging pipeline.
    :param message_text: The WhatsApp message
    :param sender_number: Twilio WhatsApp sender number (e.g. whatsapp:+14155238886)
    :param csv_bytes: Raw CSV file content in bytes
    :param sending_period: 'instant' or 'scheduled'
    :param scheduled_time: datetime object or ISO datetime string (if scheduled)
    """
    try:
        audience_data = parse_csv_content(csv_bytes)
    except Exception as e:
        raise ValueError(str(e))

    if sending_period.lower() == "instant":
        send_bulk_whatsapp(message_text, sender_number, audience_data)
        return {"status": "sent", "scheduled": False}

    elif sending_period.lower() == "scheduled":
        if not scheduled_time:
            raise ValueError("Scheduled time is required for 'scheduled' sending_period")

        # If it's a string, parse it into a datetime
        if isinstance(scheduled_time, str):
            try:
                scheduled_time = parser.isoparse(scheduled_time)
            except Exception:
                raise ValueError("Invalid datetime format. Must be ISO 8601 format.")

        # Ensure scheduled_time is in IST
        if scheduled_time.tzinfo is None:
            scheduled_time = IST.localize(scheduled_time)
        else:
            scheduled_time = scheduled_time.astimezone(IST)

        if scheduled_time <= datetime.now(IST):
            raise ValueError("Scheduled time must be in the future")

        scheduler.add_job(
            send_bulk_whatsapp,
            'date',
            run_date=scheduled_time,
            args=[message_text, sender_number, audience_data]
        )

        print(f"⏳ WhatsApp job scheduled for {scheduled_time.strftime('%Y-%m-%d %I:%M %p IST')}")
        return {"status": "scheduled", "run_time": scheduled_time.isoformat()}

    else:
        raise ValueError("Invalid sending_period. Must be 'instant' or 'scheduled'")
