from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as DjangoLoginView
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from users.forms import MyUserCreationForm

from bboard.utils import DataMixin


class MyLoginView(DataMixin,DjangoLoginView):
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
            login(request, user)  # залогиним на портал
            return redirect('home')  # перенесем на главную страницу
        # else: иначе если форма не валидная нужно вернуть форму с ошибками
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
