import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

def send_bulk_email(
    sender_email: str,
    app_password: str,
    recipients: List[str],
    subject: str,
    html_message: str
):
 
    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        for recipient in recipients:
            msg = MIMEMultipart("alternative")
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(html_message, "html"))

            server.sendmail(sender_email, recipient, msg.as_string())

        server.quit()
        print(f"Email sent successfully to {len(recipients)} recipients!")
        return {"status": "success", "sent_to": recipients}

    except Exception as e:
        print(f"Error sending email: {e}")
        return {"status": "failed", "error": str(e)}
