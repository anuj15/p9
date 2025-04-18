import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from .env_manager import get_env

EMAIL_FROM = get_env("EMAIL_FROM")
EMAIL_TO = get_env("EMAIL_TO")
EMAIL_PASSWORD = get_env("EMAIL_PASSWORD")
msg = MIMEMultipart()
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO
msg["Subject"] = "Pytest HTML Report"
ROOT_DIR = Path(__file__).resolve().parents[1]
REPORT_FILE_NAME = "basic_report.html"
REPORT_FILE_PATH = ROOT_DIR / "reports" / REPORT_FILE_NAME
LOG_FILE_NAME = "app.log"
LOG_FILE_PATH = ROOT_DIR / "logs" / LOG_FILE_NAME
SERVER = "smtp.gmail.com"
PORT = 465
body = "Hi,\n\nAttached is the latest pytest report from GitHub Actions.\n\nRegards,\nCI Bot"
msg.attach(MIMEText(body, "plain"))


def send_mail():
    with open(REPORT_FILE_PATH, "rb") as f:
        part = MIMEApplication(f.read(), Name=REPORT_FILE_NAME)
        part["Content-Disposition"] = f'attachment; filename={REPORT_FILE_NAME}'
        msg.attach(part)

    with open(LOG_FILE_PATH, "rb") as f:
        part = MIMEApplication(f.read(), Name=LOG_FILE_NAME)
        part["Content-Disposition"] = f'attachment; filename={LOG_FILE_NAME}'
        msg.attach(part)

    with smtplib.SMTP_SSL(SERVER, PORT) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
