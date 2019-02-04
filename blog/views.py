from django.shortcuts import render
from django.views.generic import DetailView, ListView
from blog.models import Article


# Create your views here.
class ArticleListView(ListView):
    queryset = Article.objects.values('title', 'date').order_by('-date')
    template_name = 'blog/article_list.html'

class ArticleDetailView(DetailView):
    queryset = Article.objects.filter()
    template_name = 'blog/article_detail.html'
    slug_field = 'slug'
