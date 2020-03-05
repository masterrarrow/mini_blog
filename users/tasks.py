from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from celery import shared_task
import logging
import os


@shared_task
def send_email(subject, email, content):
    message = Mail(
        from_email=os.environ.get("FROM_EMAIL"),
        to_emails=email,
        subject=subject,
        html_content=content)
    try:
        client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        client.send(message)
    except Exception:
        logging.warning(f"Message to {email} has not been sent")
