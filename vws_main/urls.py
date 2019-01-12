from django.contrib import admin
from django.urls import path
from django.views.generic import ListView, DetailView
from vws_main.models import Wrestler
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('table/', ListView.as_view(queryset=Wrestler.objects.all().order_by('-rating')[:10],
        template_name="vws_main/html_table.html"))
]
