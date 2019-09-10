from django.shortcuts import render

from django.http import HttpResponse

# Add the Beast class & list and view function below the imports
class Fantasticbeast:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

fantasticbeasts = [
  Fantasticbeast('Lolo', 'tabby', 'foul little demon', 3),
  Fantasticbeast('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
  Fantasticbeast('Raven', 'black tripod', '3 legged cat', 4)
]

# Define home view
def home(request):
    return HttpResponse('<h1> Hello Mr. Scamander! </h1>')

#Define about view
def about(request):
    return render(request, 'about.html')

# define index view
def fantasticbeasts_index(request):
    return render(request, 'fantasticbeasts/index.html', { 'fantasticbeasts': fantasticbeasts })