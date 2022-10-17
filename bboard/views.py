from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from .models import *

# Create your views here.

menu = ["О сайте", "Добавить объявление", "Обратная связь", "Войти"]

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def index(request):
    posts = Post.objects.all()
    return render(request, "bboard/index.html", {'title': 'Главная страница', 'menu': menu, 'posts': posts})

def about(request):
    return render(request, 'bboard/about.html', {'title': 'О сайте', 'menu': menu})

def categories(request):
    return HttpResponse("<h1>Объявления по категориям</h1>")

