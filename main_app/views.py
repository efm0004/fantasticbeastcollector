from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
@login_required
def fantasticbeasts_index(request):
  fantasticbeasts = Fantasticbeast.objects.filter(user=request.user)
  return render(request, 'fantasticbeasts/index.html', { 'fantasticbeasts': fantasticbeasts })

@login_required
def fantasticbeasts_detail(request, fantasticbeast_id):
  fantasticbeast = Fantasticbeast.objects.get(id=fantasticbeast_id)
  toys_beast_doesnt_have = Toy.objects.exclude(id__in = fantasticbeast.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'fantasticbeasts/detail.html', { 
    'fantasticbeast' : fantasticbeast, 
    'feeding_form': feeding_form,
    'toys': toys_beast_doesnt_have
    })

@login_required
def add_feeding(request, fantasticbeast_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.fantasticbeast_id = fantasticbeast_id
    new_feeding.save()
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)

class FantasticbeastCreate(LoginRequiredMixin, CreateView):
  model = Fantasticbeast
  fields = '__all__'

class FantasticbeastUpdate(LoginRequiredMixin, UpdateView):
  model = Fantasticbeast
  fields = ['breed', 'description', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class FantasticbeastDelete(LoginRequiredMixin, DeleteView):
  model = Fantasticbeast
  success_url = '/fantasticbeasts/'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, fantasticbeast_id, toy_id):
  Fantasticbeast.objects.get(id=fantasticbeast_id).toys.add(toy_id)
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)

@login_required
def unassoc_toy(request, fantasticbeast_id, toy_id):
  Fantasticbeast.objects.get(id=fantasticbeast_id).toys.remove(toy_id)
  return redirect('detail', fantasticbeast_id=fantasticbeast_id)

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
