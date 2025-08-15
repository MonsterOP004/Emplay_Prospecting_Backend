import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv(override=True)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
default_twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
whatsapp_number = os.getenv("WHATSAPP_SANDBOX_NUMBER")
client = Client(account_sid, auth_token)


def format_number(number: str, default_country_code="+91") -> str:
    """
    Format Indian and international numbers for Twilio.
    """
    number = str(number).strip()

    if number.startswith("+91") and len(number) == 13:
        return number  # Already in correct format

    if number.startswith("0"):
        number = number[1:]  # Remove leading zero

    if number.startswith("823") and len(number) == 10:
        return default_country_code + number

    if number.startswith("91") and len(number) == 12:
        return "+" + number  # Add '+' to country code

    if len(number) == 10:
        return default_country_code + number

    return number


def send_sms(body: str, to: str, from_number: str = None) -> str:

    to_number = format_number(to)
    sender = from_number or default_twilio_number

    message = client.messages.create(
        body=body,
        from_=sender,
        to=to_number
    )
    return message.sid


def send_whatsapp(body: str, to: str, from_number: str = None) -> str:

    to_number = format_number(to)
    sender = from_number or whatsapp_number
   
    message = client.messages.create(
        body=body,
        from_=f"whatsapp:{sender}",
        to=f"whatsapp:{to_number}"
    )
    return message.sid


if __name__ == "__main__":

    from_number = input("Enter sender phone number: ").strip()
    test_number = input("Enter recipient phone number: ").strip()
    message = "Hello! This is a test SMS from the updated Twilio sender."

    try:
        whatsapp_id = send_whatsapp(message, test_number, from_number=from_number)
        print(f"✅ whatsapp sent successfully! SID: {whatsapp_id}")
    except Exception as e:
        print(f"❌ SMS failed: {e}")
