from django.shortcuts import render
from django.views import generic
from .models import Newspaper
from django.shortcuts import render,get_object_or_404
# Create your views here.

class NewspapersIndexView(generic.ListView):
    template_name="news/newspapers_index.html"
    context_object_name = 'newspaper_list'

    def get_queryset(self):
        return Newspaper.objects.all()
    

def newspaper(request, pk):
    template_name="news/newspaper.html"
    newspaper = get_object_or_404(Newspaper,id=pk)
    all_news = newspaper.article_set.all()

    #Get all sections and the 6 most recent news per section
    sections = all_news.values("category").distinct()
    sections = [cat["category"] for cat in sections]
    filtered_news = dict() 
    for section in sections:
        filtered_news[section] = all_news.filter(category=section).order_by('-pub_day','-id')[0:6]
    return render(request,template_name,{
        'newspaper':newspaper,
        'filtered_news':filtered_news
    })
