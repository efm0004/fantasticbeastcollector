from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

import uuid
import boto3

from .models import Fantasticbeast, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-efm'

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
  toys_beast_doesnt_have = Toy.objects.exclude(id__in = fantasticbeast.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'fantasticbeasts/detail.html', { 
    'fantasticbeast' : fantasticbeast, 
    'feeding_form': feeding_form,
    'toys': toys_beast_doesnt_have
    })

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

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, fantasticbeast_id, toy_id):
  Fantasticbeast.objects.get(id=fantasticbeast_id).toys.add(toy_id)
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)

def unassoc_toy(request, fantasticbeast_id, toy_id):
  Fantasticbeast.objects.get(id=fantasticbeast_id).toys.remove(toy_id)
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)

def add_photo(request, fantasticbeast_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, fantasticbeast_id=fantasticbeast_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)
