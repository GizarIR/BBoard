from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('login/', LoginViewMix.as_view(), name='login'),
    path('logout/', LogoutViewMix.as_view(), name='logout'),
]