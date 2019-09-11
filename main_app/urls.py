from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for beasts index
    path('fantasticbeasts/', views.fantasticbeasts_index, name='index'),
    path('fantasticbeasts/<int:fantasticbeast_id>/', views.fantasticbeasts_detail, name='detail'),
]