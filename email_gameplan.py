import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import markdown

from content_agent import create_gameplan

NICHE = "AI Skool Community"
GOAL = "attract business owners who want to learn how to use AI — from complete beginners to those ready to build websites, ebooks, and AI agents"


def to_html(plan: str) -> str:
    body = markdown.markdown(plan, extensions=["extra"])

    return f"""
    <html>
    <head>
    <style>
        body {{ font-family: Georgia, serif; max-width: 680px; margin: 0 auto; padding: 32px 24px; color: #1a1a2e; background: #ffffff; }}
        h1 {{ font-size: 26px; color: #4f46e5; margin: 0 0 4px; }}
        h2 {{ background: #4f46e5; color: #ffffff; padding: 12px 18px; border-radius: 10px; font-size: 18px; margin: 32px 0 16px; }}
        h3 {{ font-size: 14px; font-weight: 700; color: #4f46e5; text-transform: uppercase; letter-spacing: 1px; margin: 20px 0 8px; border-left: 4px solid #4f46e5; padding-left: 10px; }}
        p {{ line-height: 1.8; margin: 6px 0; color: #374151; }}
        strong {{ color: #1a1a2e; }}
        hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 20px 0; }}
        blockquote {{ background: #f3f4f6; border-left: 4px solid #4f46e5; margin: 12px 0; padding: 12px 16px; border-radius: 0 8px 8px 0; font-style: italic; color: #374151; }}
        .header {{ border-bottom: 3px solid #4f46e5; padding-bottom: 20px; margin-bottom: 24px; }}
        .footer {{ border-top: 1px solid #e5e7eb; margin-top: 40px; padding-top: 16px; font-size: 12px; color: #9ca3af; text-align: center; }}
    </style>
    </head>
    <body>
        <div class="header">
            <h1>Your Weekly Content Plan</h1>
            <p style="margin:0;color:#6b7280;font-size:14px;">AI Skool Community — 7-Day Social Media Gameplan</p>
        </div>
        {body}
        <div class="footer">
            Generated automatically every Monday for your AI Skool Community.
        </div>
    </body>
    </html>
    """


def send_email(plan: str) -> None:
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Weekly AI Skool Content Plan"
    msg["From"] = gmail_user
    msg["To"] = gmail_user

    msg.attach(MIMEText(plan, "plain"))
    msg.attach(MIMEText(to_html(plan), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, msg.as_string())
        print("Email sent successfully.")


if __name__ == "__main__":
    print("Generating content plan...")
    plan = create_gameplan(NICHE, GOAL)
    send_email(plan)
