from django.urls import path, include
from django.contrib.auth.urls import *


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]