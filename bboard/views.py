from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index_test(request):
    return render(request, 'index.html', context={"greet":"Hello BBoard!"})