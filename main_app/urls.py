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
    path('fantasticbeasts/<int:fantasticbeast_id>/add_feeding', views.add_feeding, name='add_feeding'),
    path('fantasticbeasts/<int:fantasticbeast_id>/assoc_toy/<int:toy_id/', views.assoc_toy, name='assoc_toy'),
    path('toys/', views.ToyList.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
    path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
]