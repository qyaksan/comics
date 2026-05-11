from django.urls import path
from . import views

urlpatterns = [
    path('', views.comic_list, name='comic_list'),
    path('comic/<int:pk>/', views.comic_detail, name='comic_detail'),
    path('review/<int:review_pk>/edit/', views.edit_review, name='edit_review'),
]