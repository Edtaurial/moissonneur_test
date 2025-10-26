
from django.urls import path
from . import views

urlpatterns = [
    path('', views.page_statistiques, name='page_statistiques'),
    path('creer_admin/', views.creer_admin, name='creer_admin')
]
