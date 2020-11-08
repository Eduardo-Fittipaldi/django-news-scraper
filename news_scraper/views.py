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

    return render(request,template_name,{
        'newspaper':newspaper
    })
