from django.urls import path, include
from django.contrib.auth.urls import *

from users.views import Register, MyLoginView

urlpatterns = [
    path('login/', MyLoginView.as_view(), name="login"),
    path('register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),

]