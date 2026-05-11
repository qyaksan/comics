from django.urls import path
from . import views

urlpatterns = [
    path('export/', views.export_report, name='export_report'),
]