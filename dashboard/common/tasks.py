from django.core.mail import send_mail as _send_mail
from django.conf import settings

from dashboard.celery import app


@app.task(name='send_mail')
def send_mail(subject, message):
    _send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(settings.NOTIFIED_EMAIL,),
        fail_silently=False
    )
