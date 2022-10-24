"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', PostsView.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('addpage/', addpage, name='add_page'),
    path('addpage/', AddPostView.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post'),
    path('post/<slug:slug>/update/', PostUpdate.as_view(), name='update_post'),
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', PostsCategoryView.as_view(), name='category'),
    path('reply/<int:pk>/', ReplyDetail.as_view(), name='reply'),
    path('addreply/<slug:post_slug>/', AddReplyView.as_view(), name='add_reply'),
]

