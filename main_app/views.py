from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Fantasticbeast

# Define home view
def home(request):
  return render(request, 'home.html')

#Define about view
def about(request):
  return render(request, 'about.html')

# define index view
def fantasticbeasts_index(request):
  fantasticbeasts = Fantasticbeast.objects.all()
  return render(request, 'fantasticbeasts/index.html', { 'fantasticbeasts': fantasticbeasts })

def fantasticbeasts_detail(request, fantasticbeast_id):
  fantasticbeast = Fantasticbeast.objects.get(id=fantasticbeast_id)
  return render(request, 'fantasticbeasts/detail.html', { 'fantasticbeast' : fantasticbeast })

class FantasticbeastCreate(CreateView):
  model = Fantasticbeast
  fields = '__all__'

class FantasticbeastUpdate(UpdateView):
  model = Fantasticbeast
  fields = ['breed', 'description', 'age']

class FantasticbeastDelete(DeleteView):
  model = Fantasticbeast
  success_url = '/fantasticbeasts/'