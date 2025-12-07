from django.urls import path
from .views import JeuDeDonneesListAPIView, JeuDeDonneesDetailAPIView
from .views import ManageUserView, RegisterView
urlpatterns = [
    path('api/donnees/', JeuDeDonneesListAPIView.as_view(), name='donnees-list'),
    path('api/donnees/<int:pk>/', JeuDeDonneesDetailAPIView.as_view(), name='donnees-detail'),
    path('api/me/', ManageUserView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
]