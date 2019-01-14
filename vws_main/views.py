from django.shortcuts import render
from vws_main.models import Matchdata, Wrestler
from django.views.generic import DetailView, ListView

def home(request):
    return render(request, 'vws_main/home.html')

def contact(request):
    return render(request, 'vws_main/contact.html')

class MatchDetailView(DetailView):
    queryset = Matchdata.objects.all().filter()
    template_name = "vws_main/match_detail.html"

class MatchTableView(ListView):
    queryset = Matchdata.objects.all().order_by('-matchID')
    template_name = "vws_main/matchdata_table.html"

class WrestlerTableView(ListView):
    queryset = Wrestler.objects.all().order_by('-rating')
    template_name = "vws_main/wrestler_table.html"
