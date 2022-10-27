from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    # path('login/', LoginViewMix.as_view(), name='login'),
    path('login/', login_mix, name='login'),
    path('logout/', LogoutViewMix.as_view(), name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
]