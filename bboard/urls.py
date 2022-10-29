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
from django.urls import path

from .views import *

urlpatterns = [
    path('', PostsView.as_view(), name='home'),
    path('addpage/', AddPostView.as_view(), name='add_page'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post'),
    path('post/<slug:slug>/update/', PostUpdate.as_view(), name='update_post'),
    path('category/<slug:cat_slug>/', PostsCategoryView.as_view(), name='category'),
    path('reply/<int:pk>/', ReplyDetail.as_view(), name='reply'),
    path('addreply/<slug:post_slug>/', AddReplyView.as_view(), name='add_reply'),
    path('lk/', RepliesListSearchView.as_view(), name='replies_list_search'),
    path('lk/<int:reply_pk>/change_approved/', change_approved, name='change_approved'),
    path('lk/<int:reply_pk>/reply_delete/', reply_delete, name='reply_delete'),
]

