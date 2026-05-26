import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import markdown

from content_agent import create_gameplan

NICHE = "AI Skool Community"
GOAL = "attract business owners who want to learn how to use AI — from complete beginners to those ready to build websites, ebooks, and AI agents"


def to_plain_text(plan: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", plan)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    return text


def to_html(plan: str) -> str:
    raw_html = markdown.markdown(plan, extensions=["extra"])

    # Apply inline styles so Gmail renders them correctly
    raw_html = raw_html.replace("<h1>", '<h1 style="font-size:26px;color:#4f46e5;margin:0 0 4px;">')
    raw_html = raw_html.replace("<h2>", '<h2 style="background:#4f46e5;color:#ffffff;padding:12px 18px;border-radius:10px;font-size:18px;margin:32px 0 16px;">')
    raw_html = raw_html.replace("<h3>", '<h3 style="font-size:13px;font-weight:700;color:#4f46e5;text-transform:uppercase;letter-spacing:1px;margin:20px 0 6px;border-left:4px solid #4f46e5;padding-left:10px;">')
    raw_html = raw_html.replace("<p>", '<p style="line-height:1.8;margin:6px 0;color:#374151;">')
    raw_html = raw_html.replace("<strong>", '<strong style="color:#1a1a2e;">')
    raw_html = raw_html.replace("<hr />", '<hr style="border:none;border-top:1px solid #e5e7eb;margin:20px 0;">')

    return f"""
    <html>
    <body style="font-family:Georgia,serif;max-width:680px;margin:0 auto;padding:32px 24px;color:#1a1a2e;background:#ffffff;">
        <div style="border-bottom:3px solid #4f46e5;padding-bottom:20px;margin-bottom:24px;">
            <h1 style="font-size:26px;color:#4f46e5;margin:0 0 4px;">Your Weekly Content Plan</h1>
            <p style="margin:0;color:#6b7280;font-size:14px;">AI Skool Community &mdash; 7-Day Social Media Gameplan</p>
        </div>
        {raw_html}
        <div style="border-top:1px solid #e5e7eb;margin-top:40px;padding-top:16px;font-size:12px;color:#9ca3af;text-align:center;">
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

    msg.attach(MIMEText(to_plain_text(plan), "plain"))
    msg.attach(MIMEText(to_html(plan), "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, msg.as_string())
        print("Email sent successfully.")


if __name__ == "__main__":
    print("Generating content plan...")
    plan = create_gameplan(NICHE, GOAL)
    send_email(plan)
