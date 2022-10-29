import smtplib
from datetime import datetime, timedelta
from celery import shared_task


# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая представит наш html в виде строки

# группа импорта моделей
from .models import Post, Reply


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
