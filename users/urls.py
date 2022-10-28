from django.urls import path, include
from django.contrib.auth.urls import *

from users.views import Register

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
]