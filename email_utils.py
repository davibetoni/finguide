# ============================
# email_utils.py
# ============================
import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv


def send_email_report(subject, body):
    load_dotenv(find_dotenv())

    sender = os.environ.get("EMAIL_SENDER")
    recipient = os.environ.get("EMAIL_RECIPIENT")
    password = os.environ.get("EMAIL_PASSWORD")
    
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(body)
    print(sender, password, recipient)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.send_message(msg)
        print("✅ Email enviado com sucesso!")
