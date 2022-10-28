from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.core.exceptions import ValidationError
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator


from .forms import MyUserCreationForm, MyAuthenticationForm

from bboard.utils import DataMixin
from .utils import send_email_for_verify, check_code

User = get_user_model()

class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        # # Проверка при реализации проверки емейла через ссылку
        # if user is not None and token_generator.check_token(user, token):
        #     user.email_verify = True
        #     user.save()
        #     login(request, user)
        #     return redirect('home')
        # return redirect('invalid_verify')

        # Проверка при реализации проверки емейла через code


        if user is not None and check_code(user, code):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
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

class MyLoginView(DataMixin,DjangoLoginView):
    form_class = MyAuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход на портал")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class Register(DataMixin, View):

    template_name = 'registration/register.html'

    def get(self, request):
        # context = {
        #     'form': UserCreationForm
        # }
        # form = self.form_class()
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
            form.save()  # сохраним пользователя
            # username = form.cleaned_data.get('username')  # получим из сохраненных данных логин и пароль
            email = form.cleaned_data.get('email')  # передалаем на email (в моделях тоже внесли изменения)
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)  # аутентифицируем его (поменяли на email)
            # # для логирования пользователя без подтверждения емейла используй код ниже
            # login(request, user)  # залогиним на портал
            # return redirect('home')  # перенесем на главную страницу
            # для реализации подтверждения пользовательского емейла используй код нижже
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        # else: иначе если форма не валидная нужно вернуть форму с ошибками
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
