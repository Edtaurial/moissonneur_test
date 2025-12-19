from graphene_django import DjangoObjectType
from moissonneur.models import JeuDeDonnees
import graphene

class JeuDeDonneesType(DjangoObjectType):
    class Meta:
        model = JeuDeDonnees
        fields = '__all__'

class Query(graphene.ObjectType):
    # 1. On déclare les arguments acceptés pour la liste
    tous_les_jeux = graphene.List(
        JeuDeDonneesType, 
        organisation=graphene.String(),
        first=graphene.Int(),
        titre_contains=graphene.String()
    )
    
    # 2. On déclare le champ pour un élément unique
    jeu_de_donnees = graphene.Field(JeuDeDonneesType, id=graphene.Int(required=True))

    # Resolveur pour la liste (Gère les filtres et la limite)
    def resolve_tous_les_jeux(self, info, organisation=None, first=None, titre_contains=None):
        qs = JeuDeDonnees.objects.all()
        
        if organisation:
            qs = qs.filter(organisation=organisation)
            
        if titre_contains:
            qs = qs.filter(titre__icontains=titre_contains)
            
        if first:
            qs = qs[:first] # Applique la limite (ex: first: 10)
            
        return qs

    # Resolveur pour l'élément unique
    def resolve_jeu_de_donnees(self, info, id):
        try:
            return JeuDeDonnees.objects.get(pk=id)
        except JeuDeDonnees.DoesNotExist:
            return None
schema = graphene.Schema(query=Query)