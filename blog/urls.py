from django.contrib import admin
from django.urls import path
from django.views.generic import ListView, DetailView
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('<slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
]
