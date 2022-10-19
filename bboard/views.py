from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .forms import AddPostForm
from .models import *

# Create your views here.

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить объявление", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def about(request):
    return render(request, 'bboard/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def index(request):
    posts = Post.objects.all()
    cats = Category.objects.all()
    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'bboard/index.html', context=context)

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': 1,
    }

    return render(request, 'bboard/post.html', context=context)


def show_category(request, cat_slug):
    posts = Post.objects.filter(category__slug=cat_slug)
    if len(posts) == 0:
        raise Http404()
    # cats = Category.objects.all() # заменено на тэг get_categories
    context = {
        'posts': posts,
        # 'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': cat_slug,
    }
    # print(context)
    return render(request, 'bboard/index.html', context=context)


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            try:
                form.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()

    return render(request, 'bboard/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})