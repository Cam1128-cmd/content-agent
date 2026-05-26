import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from content_agent import create_gameplan

NICHE = "AI Skool Community"
GOAL = "attract business owners who want to learn how to use AI — from complete beginners to those ready to build websites, ebooks, and AI agents"


def to_html(plan: str) -> str:
    lines = plan.splitlines()
    html_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## ") or stripped.startswith("# "):
            text = re.sub(r"^#{1,2} ", "", stripped)
            html_lines.append(f'<h2 style="color:#1a1a2e;margin-top:28px;margin-bottom:6px;font-size:18px;">{text}</h2>')

        elif stripped.startswith("- "):
            text = stripped[2:].strip()
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            html_lines.append(f'<p style="margin:4px 0 4px 16px;">&#8226; {text}</p>')

        elif stripped == "":
            html_lines.append("<br>")

        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            html_lines.append(f'<p style="margin:6px 0;">{text}</p>')

    body = "\n".join(html_lines)

    return f"""
    <html>
    <body style="font-family:Georgia,serif;max-width:680px;margin:0 auto;padding:32px 24px;color:#1a1a2e;background:#ffffff;">
        <div style="border-bottom:3px solid #4f46e5;padding-bottom:16px;margin-bottom:24px;">
            <h1 style="margin:0;font-size:24px;color:#4f46e5;">Your Weekly AI Skool Content Plan</h1>
        </div>
        {body}
        <div style="border-top:1px solid #e5e7eb;margin-top:32px;padding-top:16px;font-size:13px;color:#6b7280;">
            Generated automatically for your AI Skool Community.
        </div>
    </body>
    </html>
    """


def send_email(plan: str) -> None:
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your 7-Day AI Skool Content Plan"
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
