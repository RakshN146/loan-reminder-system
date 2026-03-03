import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")


def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()

        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False