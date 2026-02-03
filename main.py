from fastapi import FastAPI
from dotenv import load_dotenv
import os
from mail_service import read_mail_by_subject, send_mail

load_dotenv()

app = FastAPI(title="Mail Automation API")

IMAP_SERVER = os.getenv("IMAP_SERVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


@app.get("/read-mails")
def read_mails(subject: str):
    attachments = read_mail_by_subject(
        subject,
        IMAP_SERVER,
        EMAIL_ID,
        EMAIL_PASSWORD
    )
    return {
        "status": "success",
        "attachments_downloaded": attachments
    }


@app.post("/send-mail")
def send_email_api(
    to_email: str,
    subject: str,
    body: str,
):
    attachment_files = os.listdir("attachments")
    attachment_paths = [f"attachments/{f}" for f in attachment_files]

    send_mail(
        to_email,
        subject,
        body,
        attachment_paths,
        SMTP_SERVER,
        SMTP_PORT,
        EMAIL_ID,
        EMAIL_PASSWORD
    )

    return {"status": "Mail sent successfully"}
