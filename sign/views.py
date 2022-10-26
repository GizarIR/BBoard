from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from bboard.utils import *

# Create your views here.


class LoginViewMix(DataMixin, LoginView):
    template_name = 'sign/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


class LogoutViewMix(DataMixin, LogoutView):
    template_name = 'sign/logout.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Выход с портала")
        return dict(list(context.items()) + list(c_def.items()))
