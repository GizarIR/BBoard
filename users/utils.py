import random

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from bboard.models import OneTimeCode


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
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    email=EmailMessage(
        'Подтвердите свой email',
        message,
        to=[user.email],
    )
    email.send()