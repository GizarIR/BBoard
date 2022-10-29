from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Reply, Post, User
from project.settings import USE_CELERY_SEND_EMAIL
from .tasks import send_email_reply_celery

def send_email_reply(user_to_email, post, reply, title_email, template):
    "Отправка уведомлений на email выбранным способом в зависимости от настроек"
    print(f'Подготовлен к отправке список для Celery: {user_to_email[0]}')
    if user_to_email[0] is not None:
        html_content = render_to_string(
            template,
            {
                'reply': reply,
                'post': post,
                'username': user_to_email[2] if user_to_email[2] else user_to_email[1],
            }
        )
        if not USE_CELERY_SEND_EMAIL:
            # Синхронно
            msg = EmailMultiAlternatives(
                subject=title_email,
                body=reply.text,
                from_email='gizarir@mail.ru',
                to=[user_to_email[0], ],
            )
            msg.attach_alternative(html_content, "text/html")
            print(f'Отправка письма подписчику {user_to_email[0]}...')
            msg.send()
        else:
            # запускаем асинхронно для каждого отправления Celery
            send_email_reply_celery.delay(user_to_email, title_email, html_content)
    else:
        print('Email для отправки не найден')
    return

@receiver(post_save, sender=Reply)
def notify_change_reply(sender, instance, created, **kwargs):
    """Перехват сигнала для уведомления о создании и изменениях в отклике"""
    reply = instance
    post = Post.objects.get(pk=instance.post.pk)
    author_reply = (reply.user.email, reply.user.username, reply.user.first_name)
    author_post = (post.user.email, post.user.username, post.user.first_name)

    if created:
        subject_email = f'Новый отклик на Ваше объявление'
        send_email_reply(author_post, post, reply, subject_email, 'reply_created.html')
    else:
        subject_email = f'Изменение статуса Вашего отклика на портале Bboard'
        send_email_reply(author_reply, post, reply, subject_email, 'reply_is_approved.html')
    return
