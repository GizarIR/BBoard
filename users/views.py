from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreationForm


class Register(View):

    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm
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


