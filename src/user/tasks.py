from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def confirm_email(message, email):
    email = EmailMessage(
        "Подтверждение почты",
        message,
        to=[email],
    )
    email.send()
