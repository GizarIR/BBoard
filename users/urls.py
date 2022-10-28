from django.urls import path, include
from django.contrib.auth.urls import *
from django.views.generic import TemplateView

from .views import Register, MyLoginView, ConfirmEmail

urlpatterns = [
    path('login/', MyLoginView.as_view(), name="login"),
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='registration/invalid_verify.html'),
        name='invalid_verify'
    ),
    path(
        'verify_email/',
        EmailVerify.as_view(),
        name='verify_email',
    ),
    path('confirm_email/', ConfirmEmail.as_view(), name='confirm_email'),

]