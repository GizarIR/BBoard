from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views.generic import TemplateView

from .forms import MyUserCreationForm, MyAuthenticationForm, EmailVerifyForm

from bboard.utils import DataMixin
from .utils import send_email_for_verify, check_code, clear_old_code
from bboard.tasks import send_email_for_verify_celery
from project.settings import USE_CELERY_SEND_EMAIL


User = get_user_model()


class InvalidVerifyView(DataMixin, TemplateView):
    """View for present information when check code is not valid """
    template_name = 'registration/invalid_verify.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Некорректная ссылка или введенный код")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ConfirmEmailView(DataMixin, TemplateView):
    """View for present information when one time code sent to email """
    template_name = 'registration/confirm_email.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Проверьте Ваш email")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class EmailVerify(DataMixin, View):
    """View for form check email and code valid"""
    template_name = 'registration/verify_email_form.html'

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        categories = self.get_user_context()['categories']
        menu = self.get_user_context()['menu']
        cat_selected = self.get_user_context()['cat_selected']
        context = {
            'user': user,
            'uid': uidb64,
            'token': token,
            'form': EmailVerifyForm,
            'menu': menu,
            'categories': categories,
            'cat_selected': cat_selected,
        }
        return render(request, self.template_name, context)

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        form = EmailVerifyForm(request.POST)

        if form.is_valid():
            if user is not None and token_generator.check_token(user, token):
                code = form.cleaned_data.get('code')
                if check_code(code, user):
                    user.email_verify = True
                    user.is_staff = True
                    user.save()
                    login(request, user)
                    return redirect('home')
        # else: иначе если форма не валидная нужно вернуть форму с ошибками
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class MyLoginView(DataMixin, DjangoLoginView):
    form_class = MyAuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход на портал")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Register(DataMixin, View):
    """View for registration form with email """
    template_name = 'registration/register.html'

    def get(self, request):
        categories = self.get_user_context()['categories']
        menu = self.get_user_context()['menu']
        cat_selected = self.get_user_context()['cat_selected']
        # print(post_slug)
        context = {
            'form': MyUserCreationForm,
            'menu': menu,
            'categories': categories,
            'cat_selected': cat_selected,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MyUserCreationForm(request.POST)

        if form.is_valid():  # если данные в форме правильные
            form.save()  # сохраним форму и пользователя
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            clear_old_code(user)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        # else: иначе если форма не валидная нужно вернуть форму с ошибками
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
