from graphene_django import DjangoObjectType
from moissonneur.models import JeuDeDonnees
import graphene

class JeuDeDonneesType(DjangoObjectType):
    class Meta:
        model = JeuDeDonnees
        fields = '__all__'

class Query(graphene.ObjectType):
    all_jeu_donnees = graphene.List(JeuDeDonneesType)

    jeu_donnees_by_id = graphene.Field(JeuDeDonneesType, id=graphene.Int(required=True))


    def resolve_all_jeu_donnees(self, info, **kwargs):
        return JeuDeDonnees.objects.all()

    def resolve_jeu_donnees_by_id(root, info, id):
        try:
            return JeuDeDonnees.objects.get(pk=id)
        except JeuDeDonnees.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)