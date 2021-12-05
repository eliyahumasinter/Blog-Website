from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import os

sender_email = os.envorn['EMAIL']
password = os.environ['PASSWORD']


def send_notifications(email, title):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"New Post ({title}) on Eliyahu's Blog!"
    message["From"] = sender_email
    message["To"] = email
    text = "Eliyahu has posted a new post on his blog. You can view it here: eliyahumasinter.com"
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, email,
                            message.as_string())
    except:
        print("ERROR SENDING EMAIL TO", email)
