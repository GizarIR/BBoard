import random

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from project.bboard.models import OneTimeCode

def check_code(user, code):
    pass

def generate_code(user):
    OneTimeCode.objects.create(code=random.choice('1234567890'), user=user)

def send_email_for_verify(request, user):
    context = {
        'user': user,
        "code": generate_code(user),
    }
    message = render_to_string(
        'registration/verify_code_email.html',
        context=context,
    )
    email=EmailMessage(
        'Код подтверждения email',
        message,
        to=[user.email],
    )
    email.send()
