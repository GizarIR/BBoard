from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


from bboard.models import *

def check_code(user, code):
    pass

def generate_code(user):
    pass

def send_email_for_verify(request, user):
    context = {
        'user': user,
        "code": generate_code(user),
    }
    message = render_to_string(
        'registration/verify_email.html',
        context=context,
    )
    email=EmailMessage(
        'Verify email',
        message,
        to=[user.email],
    )
    email.send()
