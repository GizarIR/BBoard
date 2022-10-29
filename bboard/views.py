from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import PostForm, AddReplyForm
from .utils import *
from .filters import *
from .models import *


def reply_delete(request, reply_pk):
    """Delete reply"""
    reply = get_object_or_404(Reply, pk=reply_pk)
    reply.delete()
    return redirect('replies_list_search')


def change_approved(request, reply_pk):
    """Change status reply"""
    reply = get_object_or_404(Reply, pk=reply_pk)
    reply.is_approved = False if reply.is_approved else True
    reply.save()
    return redirect('replies_list_search')


class RepliesListSearchView(DataMixin, ListView):
    """The view returns a list of replies for use in the personal account"""
    model = Reply
    ordering = '-time_create'
    template_name = 'replies_search.html'
    context_object_name = 'finded_replies'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(post__user=self.request.user)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        c_def = self.get_user_context(title="Поиск откликов:")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class PostUpdate(DataMixin, UpdateView):
    """View for edit post"""
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        post = form.save(commit=False)
        post.is_created = False
        return super().form_valid(form)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ReplyDetail(DataMixin, DetailView):
    """View for detail of reply"""
    model = Reply
    template_name = 'bboard/reply.html'
    context_object_name = 'reply'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Отклик на объявление")
        return dict(list(context.items()) + list(c_def.items()))


class PostsView(DataMixin, ListView):
    """View for list the posts on main board"""
    model = Post
    template_name = 'bboard/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            qs = Post.objects.filter(is_published=True).order_by('-time_update')
        else:
            qs = Post.objects.filter(Q(is_published=True) | Q(user=self.request.user)).order_by('-time_update')
        return qs


class PostsCategoryView(DataMixin, ListView):
    """View for show posts by category"""
    model = Category
    template_name = 'bboard/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].category),
                                      cat_selected=context['posts'][0].category.slug)
        return dict(list(context.items()) + list(c_def.items()))


class PostDetail(DataMixin, DetailView):
    """View for read post"""
    model = Post
    template_name = 'bboard/post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class AddPostView(LoginRequiredMixin, DataMixin, CreateView):
    """View for add post"""
    form_class = PostForm
    template_name = 'bboard/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление объявления")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = User.objects.get(username=self.request.user)
        return super().form_valid(form)


class AddReplyView(LoginRequiredMixin, DataMixin, View):
    """View for add reply """
    form_class = AddReplyForm
    template_name = 'bboard/reply_add.html'

    def get(self, request, post_slug, *args, **kwargs):
        form = self.form_class()
        categories = self.get_user_context()['categories']
        menu = self.get_user_context()['menu']
        cat_selected = self.get_user_context()['cat_selected']
        print(post_slug)
        context = {
            'form': form,
            'menu': menu,
            'categories': categories,
            'cat_selected': cat_selected,
            'post_slug': post_slug,
        }
        return render(request, self.template_name, context=context )

    def post(self, request, post_slug, *args, **kwargs):
        form = self.form_class(request.POST)
        reply = request.POST
        if form.is_valid():
            Reply.objects.create(
                user=User.objects.get(username=self.request.user),
                post=Post.objects.get(slug=post_slug),
                text=reply['text'],
                is_approved=True
            )
            return redirect('post', slug=post_slug)
        return render(request, self.template_name, {'form': form})
