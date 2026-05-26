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
    in_script = False

    for line in lines:
        stripped = line.strip()

        # Day header (# Day 1 — Theme)
        if re.match(r"^# Day", stripped):
            in_script = False
            text = stripped.lstrip("# ").strip()
            html_lines.append(
                f'<div style="background:#4f46e5;color:#ffffff;padding:14px 20px;border-radius:10px;margin:32px 0 16px;">'
                f'<h2 style="margin:0;font-size:20px;letter-spacing:0.3px;">{text}</h2></div>'
            )

        # Post header (## Post 1)
        elif re.match(r"^## Post", stripped):
            in_script = False
            text = stripped.lstrip("# ").strip()
            html_lines.append(
                f'<h3 style="color:#1a1a2e;font-size:16px;margin:24px 0 8px;border-bottom:1px solid #e5e7eb;padding-bottom:6px;">{text}</h3>'
            )

        # Video script header
        elif re.match(r"^### Video Script", stripped):
            in_script = True
            html_lines.append(
                '<div style="background:#f3f4f6;border-left:4px solid #4f46e5;padding:14px 18px;border-radius:0 8px 8px 0;margin:12px 0;">'
                '<p style="margin:0 0 8px;font-size:12px;font-weight:700;color:#4f46e5;text-transform:uppercase;letter-spacing:1px;">Video Script</p>'
            )

        # Divider closes script block
        elif stripped == "---":
            if in_script:
                html_lines.append("</div>")
                in_script = False
            html_lines.append('<hr style="border:none;border-top:1px solid #e5e7eb;margin:20px 0;">')

        # Bold labels: **Hook:** **Value:** **CTA:**
        elif re.match(r"^\*\*(Hook|Value|CTA):\*\*", stripped):
            label = re.match(r"^\*\*(.+?):\*\*", stripped).group(1)
            html_lines.append(
                f'<p style="margin:10px 0 2px;font-size:12px;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.8px;">{label}</p>'
            )

        # Empty line
        elif stripped == "":
            if not in_script:
                html_lines.append('<div style="height:6px;"></div>')

        # Regular text (inside script or normal paragraph)
        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            if in_script:
                html_lines.append(f'<p style="margin:4px 0;font-style:italic;color:#374151;line-height:1.7;">{text}</p>')
            else:
                html_lines.append(f'<p style="margin:4px 0;color:#374151;line-height:1.7;">{text}</p>')

    if in_script:
        html_lines.append("</div>")

    body = "\n".join(html_lines)

    return f"""
    <html>
    <body style="font-family:Georgia,serif;max-width:680px;margin:0 auto;padding:32px 24px;color:#1a1a2e;background:#ffffff;">
        <div style="border-bottom:3px solid #4f46e5;padding-bottom:20px;margin-bottom:8px;">
            <h1 style="margin:0 0 4px;font-size:26px;color:#4f46e5;">Your Weekly Content Plan</h1>
            <p style="margin:0;color:#6b7280;font-size:14px;">AI Skool Community &mdash; 7-Day Social Media Gameplan</p>
        </div>
        {body}
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
