import smtplib
from datetime import datetime, timedelta
from celery import shared_task
# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_email_reply_celery(user_to_email, title_email, html_content):

    msg = EmailMultiAlternatives(
        subject=title_email,
        body="",
        from_email='gizarir@mail.ru',
        to=[user_to_email[0], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f'Отправка письма подписчику {user_to_email[0]}...')
    msg.send()
    return

@shared_task
def send_email_for_verify_celery(html_content, user_to_email):
    msg = EmailMultiAlternatives(
        subject='Подтвердите свой email',
        body="",
        from_email='gizarir@mail.ru',
        to=[user_to_email[0], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f'Отправка письма подписчику {user_to_email[0]}...')
    msg.send()
