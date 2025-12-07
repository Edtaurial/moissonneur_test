
from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_statistiques, name='page_statistiques'),
]