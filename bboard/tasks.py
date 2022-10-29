import smtplib
from datetime import datetime, timedelta
from celery import shared_task


# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая представит наш html в виде строки

# группа импорта моделей
from .models import Post, Reply


@shared_task
def send_email_reply_celery(post_pk, subject_email, subscriber, html_content):
    post = Post.objects.get(pk=post_pk)

    msg = EmailMultiAlternatives(
        subject=subject_email,
        body=post.text_post,
        from_email='gizarir@mail.ru',
        to=[subscriber[0], ],
    )
    msg.attach_alternative(html_content, "text/html")

    print(_(f'Sending a message to the subscriber {subscriber[0]}...')) #f'Отправка письма подписчику {subscriber[0]}...

    msg.send()
    return
