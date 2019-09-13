from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Fantasticbeast
from .forms import FeedingForm

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
  feeding_form = FeedingForm()
  return render(request, 'fantasticbeasts/detail.html', { 
    'fantasticbeast' : fantasticbeast, 
    'feeding_form': feeding_form})

def add_feeding(request, fantasticbeast_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.fantasticbeast_id = fantasticbeast_id
    new_feeding.save()
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)

class FantasticbeastCreate(CreateView):
  model = Fantasticbeast
  fields = '__all__'

class FantasticbeastUpdate(UpdateView):
  model = Fantasticbeast
  fields = ['breed', 'description', 'age']

class FantasticbeastDelete(DeleteView):
  model = Fantasticbeast
  success_url = '/fantasticbeasts/'