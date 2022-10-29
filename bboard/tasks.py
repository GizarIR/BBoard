from django.core.mail import EmailMultiAlternatives

from celery import shared_task


@shared_task
def send_email_reply_celery(user_to_email, title_email, html_content):
    """Function send email by Celery when model reply change in app bbooard """
    msg = EmailMultiAlternatives(
        subject=title_email,
        body="",
        from_email='gizarir@mail.ru',
        to=[user_to_email[0], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f'Отправка письма автору {user_to_email[0]}...')
    msg.send()
    return


@shared_task
def send_email_for_verify_celery(html_content, user_to_email):
    """Function send email by Celery when user model change in app users """
    msg = EmailMultiAlternatives(
        subject='Подтвердите свой email',
        body="",
        from_email='gizarir@mail.ru',
        to=[user_to_email[0], ],
    )
    msg.attach_alternative(html_content, "text/html")
    print(f'Отправка письма пользователю {user_to_email[0]}...')
    msg.send()
