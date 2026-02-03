import imaplib
import email
from email.message import EmailMessage
import smtplib
import os

ATTACHMENT_DIR = "attachments"
os.makedirs(ATTACHMENT_DIR, exist_ok=True)


def read_mail_by_subject(subject, imap_server, email_id, password):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_id, password)
    mail.select("inbox")

    status, messages = mail.search(None, f'(SUBJECT "{subject}")')
    email_ids = messages[0].split()

    attachments = []

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                filepath = os.path.join(ATTACHMENT_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                attachments.append(filepath)

    mail.logout()
    return attachments


def send_mail(to_email, subject, body, attachment_paths, smtp_server, smtp_port, email_id, password):
    msg = EmailMessage()
    msg["From"] = email_id
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    for file_path in attachment_paths:
        with open(file_path, "rb") as f:
            file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=os.path.basename(file_path))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_id, password)
        server.send_message(msg)
