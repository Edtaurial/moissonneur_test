from django.urls import path
from .views import JeuDeDonneesListAPIView, JeuDeDonneesDetailAPIView

urlpatterns = [
    path('api/donnees/', JeuDeDonneesListAPIView.as_view(), name='donnees-list'),
    path('api/donnees/<int:pk>/', JeuDeDonneesDetailAPIView.as_view(), name='donnees-detail'),
]