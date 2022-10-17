from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.

def index(request):
    return HttpResponse("Доска объявлений")

def categories(request):
    return HttpResponse("<h1>Объявления по категориям</h1>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')