from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View


from .forms import AddPostForm, AddReplyForm
from .models import *
from .utils import *


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def about(request):
    return render(request, 'bboard/about.html', {'menu': menu, 'title': 'О сайте'})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

# def index(request):
#     posts = Post.objects.all()
#     cats = Category.objects.all()
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'bboard/index.html', context=context)
#
# def show_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': 1,
#     }
#     return render(request, 'bboard/post.html', context=context)
#
# def show_category(request, cat_slug):
#     posts = Post.objects.filter(category__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()
#     # cats = Category.objects.all() # заменено на тэг get_categories
#     context = {
#         'posts': posts,
#         # 'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': cat_slug,
#     }
#     # print(context)
#     return render(request, 'bboard/index.html', context=context)
#
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             try:
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'bboard/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


class ReplyDetail(DataMixin, DetailView):
    model = Reply
    template_name = 'bboard/reply.html'
    # slug_url_kwarg = 'post_slug' # используй если нужно переименовать переменную для вьюшки - по умолчанию slug
    context_object_name = 'reply'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Отклик на объявление")
        return dict(list(context.items()) + list(c_def.items()))

class PostsView(DataMixin, ListView):
    model = Post
    template_name = 'bboard/index.html'
    context_object_name = 'posts'
    # extra_context = {'title' : 'Главная страница'}  # для статичных данных
    # paginate_by = 3 # определен в DataMixin

    #  Добавляем контекст в шаблоны
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    # Добавим параметры выборки данных для шаблонов
    # отображаем только те что опубликованы
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-time_update')

class PostsCategoryView(DataMixin, ListView):
    model = Category
    template_name = 'bboard/index.html'
    context_object_name = 'posts'
    allow_empty = False # выдаем ошибку 404 если выборка пуста

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].category),
                                      cat_selected=context['posts'][0].category.slug)
        return dict(list(context.items()) + list(c_def.items()))


class PostDetail(DataMixin, DetailView):
    model = Post
    template_name = 'bboard/post.html'
    # slug_url_kwarg = 'post_slug' # используй если нужно переименовать переменную для вьюшки - по умолчанию slug
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class AddPostView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'bboard/addpage.html'
    success_url = reverse_lazy('home') # по умолчанию на страницу просмотра деталей
    login_url = reverse_lazy('home')
    # raise_exception = True # если нужно будет генерить исключение при неавторизованном пользователе

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление объявления")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(author_user=self.request.user)
        return super().form_valid(form)

class AddReplyView(DataMixin, View):
    form_class = AddReplyForm
    # initial = {'post_id': ''}
    template_name = 'bboard/reply_add.html'

    def get(self, request, post_slug, *args, **kwargs):
        # self.initial = post_id
        # form = self.form_class(initial=self.initial)
        form = self.form_class()
        categories = self.get_user_context()['categories']
        menu = self.get_user_context()['menu']
        cat_selected = self.get_user_context()['cat_selected']
        print(post_slug)
        context = {'form': form, 'menu': menu, 'categories': categories, 'cat_selected':cat_selected, 'post_slug': post_slug}
        return render(request, self.template_name, context=context )


    def post(self, request, post_slug, *args, **kwargs):
        form = self.form_class(request.POST)
        reply = request.POST
        if form.is_valid():
            # <process form cleaned data>
            # print(reply['is_approved'])
            Reply.objects.create(
                author = Author.objects.get(author_user=self.request.user),
                post = Post.objects.get(slug=post_slug),
                text = reply['text'],
                is_approved = True
            )
            return redirect('post', slug=post_slug)
        return render(request, self.template_name, {'form': form})
