import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from content_agent import create_gameplan

NICHE = "AI Skool Community"
GOAL = "attract business owners who want to learn how to use AI — from complete beginners to those ready to build websites, ebooks, and AI agents"


def send_email(plan: str) -> None:
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your 7-Day AI Skool Content Plan"
    msg["From"] = gmail_user
    msg["To"] = gmail_user

    msg.attach(MIMEText(plan, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, msg.as_string())
        print("Email sent successfully.")


if __name__ == "__main__":
    print("Generating content plan...")
    plan = create_gameplan(NICHE, GOAL)
    send_email(plan)
