from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreationForm

from bboard.utils import DataMixin

class LoginView(DataMixin,LoginView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход на портал")
        context = dict(list(context.items()) + list(c_def.items()))
        print(context)
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
            'form': UserCreationForm,
            'menu': menu,
            'categories': categories,
            'cat_selected':cat_selected,
            # 'post_slug': post_slug
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():  # если данные в форме правильные
            form.save()  # сохраним пользователя
            username = form.cleaned_data.get('username')  # получим из сохраненных данных логин и пароль
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)  # аутентифицируем его
            login(request, user)  # залогиним на портал
            return redirect('home')  # перенесем на главную страницу
        # else: иначе если форма не валидная нужно вернуть форму с ошибками
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


