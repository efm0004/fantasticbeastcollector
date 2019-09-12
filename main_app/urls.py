from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for beasts index
    path('fantasticbeasts/', views.fantasticbeasts_index, name='index'),
    path('fantasticbeasts/<int:fantasticbeast_id>/', views.fantasticbeasts_detail, name='detail'),
    path('fantasticbeasts/create/', views.FantasticbeastCreate.as_view(), name='fantasticbeasts_create'),
    path('fantasticbeasts/<int:pk>/update/', views.FantasticbeastUpdate.as_view(), name='fantasticbeasts_update'),
    path('fantasticbeasts/<int:pk>/delete/', views.FantasticbeastDelete.as_view(), name='fantasticbeasts_delete'),
]