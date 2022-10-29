from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Reply, Post

def send_email_for_reply(user_to_email, post, reply, title_email, template):
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

        # запускаем асинхронно для каждого отправления Celery
        # send_mails_new_pub.delay(post.id, subject_email, [subscriber[0],], html_content)

        # Ниже код ("commented") перенесен в задачи tasks.py для усовершенствования и
        # отправки писем при помощи асинхронной модели с использованием Celery и Redis
        msg = EmailMultiAlternatives(
            subject=title_email,
            body=reply.text,
            from_email='gizarir@mail.ru',
            to=[user_to_email[0],],
        )
        msg.attach_alternative(html_content, "text/html")
        print(f'Отправка письма подписчику {user_to_email[0]}...')
        msg.send()


@receiver(post_save, sender=Reply)
def notify_managers_appointment(sender, instance, created, **kwargs):
    """Уведомление подписчиков о выходе новой публикации в категории"""
    reply = instance
    post = Post.objects.get(pk=instance.post.pk)
    author_reply = (reply.user.email, reply.user.username, reply.user.first_name)
    author_post = (post.user.email, post.user.username, post.user.first_name)

    if created:
        subject_email=f'Новый отклик на Ваше объявление'
        send_email_for_reply(author_post, post, reply, subject_email, 'reply_created.html')
    else:
        subject_email = f'Изменение статуса Вашего отклика на портале Bboard'
        send_email_for_reply(author_reply, post, reply, subject_email, 'reply_is_approved.html')
    return