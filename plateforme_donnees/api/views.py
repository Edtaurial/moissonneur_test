from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from moissonneur.models import JeuDeDonnees
from .serializer import JeuDeDonneesSerializer
from drf_yasg.utils import swagger_auto_schema

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework import generics

# vue pour la liste des jeux de donnees
class JeuDeDonneesListAPIView(APIView):
    """
    Lister tous les jeux de données.
    """
    #secrurisation de la vue
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['JeuDeDonnees'], responses={200: JeuDeDonneesSerializer(many=True)})
    def get(self, request, format=None):
        jeux = JeuDeDonnees.objects.all()
        serializer = JeuDeDonneesSerializer(jeux, many=True, context={'request': request})
        return Response(serializer.data)

# vue pour le détail d un seul jeu de donneees
class JeuDeDonneesDetailAPIView(APIView):
    """
    Récupérer un jeu de données spécifique par son ID.
    """
    # secrurisation de la vue
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(tags=['JeuDeDonnees'], responses={200: JeuDeDonneesSerializer, 404: 'Not Found'})
    def get_object(self, pk):
        try:
            return JeuDeDonnees.objects.get(pk=pk)
        except JeuDeDonnees.DoesNotExist:
            raise Http404  #return None

    def get(self, request, pk, format=None):
        jeu = self.get_object(pk)
        serializer = JeuDeDonneesSerializer(jeu)
        return Response(serializer.data)


# vue pour la création d'un utilisateur
class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Créer un nouvel utilisateur.
    """
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retourne directement l'utilisateur connecté via le token
        return self.request.user

# NOUVEAU : Vue d'inscription (ouverte à tous)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]