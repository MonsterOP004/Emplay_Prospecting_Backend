# tools/twilio_messenger.py

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv(override=True)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(account_sid, auth_token)

def send_sms(body: str, to: str) -> str:
    
    message = client.messages.create(
        body=body,
        from_=twilio_number,
        to=to
    )
    return message.sid

def send_whatsapp(body: str, to: str) -> str:
    
    message = client.messages.create(
        body=body,
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{to}"
    )
    return message.sid

if __name__ == "__main__":
    # Simple test to check SMS and WhatsApp sending
    test_number = input("Enter recipient phone number (with country code, e.g., +919876543210): ")

    message = """"Technology has significantly transformed the way we live, work, and communicate. In today’s digital world, access to information is just a click away. From"""

    try:
        sms_sid = send_sms(message, test_number)
        print(f"✅ SMS sent successfully! SID: {sms_sid}")
    except Exception as e:
        print(f"❌ SMS failed: {e}")

    # try:
    #     whatsapp_sid = send_whatsapp("Hello from Twilio WhatsApp!", test_number)
    #     print(f"✅ WhatsApp message sent successfully! SID: {whatsapp_sid}")
    # except Exception as e:
    #     print(f"❌ WhatsApp failed: {e}")
