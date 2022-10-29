import random

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from bboard.models import OneTimeCode
from bboard.tasks import send_email_for_verify_celery
from project.settings import USE_CELERY_SEND_EMAIL


def clear_old_code(user):
    OneTimeCode.objects.filter(user=user).delete()


def check_code(code, user):
    if user is not None and OneTimeCode.objects.filter(user=user).exists():
        if code == OneTimeCode.objects.get(user=user).code:
            return True
    return False

def generate_code(user):
    code = ''.join(random.choices('0123456789', k=4))
    OneTimeCode.objects.create(code=code, user=user)
    return code

def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),
        "code": generate_code(user),
    }
    html_content = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    user_to_email=(user.email, user.username, user.first_name)
    if not USE_CELERY_SEND_EMAIL:
        email=EmailMessage(
            'Подтвердите свой email',
            html_content,
            to=[user.email],
        )
        email.send()
        return print('Email отправлен синхронно')
    else:
        send_email_for_verify_celery.delay(html_content, user_to_email)
        return print('Email отправлен в Celery для асинхронной отправки')
