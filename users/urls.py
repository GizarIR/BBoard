from django.urls import path, include
from django.contrib.auth.urls import *

from .views import Register, MyLoginView, EmailVerify, ConfirmEmailView, InvalidVerifyView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name="login"),
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path(
        'invalid_verify/',
        InvalidVerifyView.as_view(),
        name='invalid_verify'
    ),
    path(
        'verify_email/<uidb64>/<token>/',
        EmailVerify.as_view(),
        name='verify_email',
    ),
    path('confirm_email/', ConfirmEmailView.as_view() , name='confirm_email'),
]
