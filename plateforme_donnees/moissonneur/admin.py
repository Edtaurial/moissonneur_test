from django.contrib import admin
from .models import JeuDeDonnees



@admin.register(JeuDeDonnees)
class JeuDeDonneesAdmin(admin.ModelAdmin):
    list_affichage = ('titre', 'source_catalogue', 'organisation', 'date_maj_plateforme')
    list_filtre = ('source_catalogue', 'organisation')
    champs_recherche = ('titre', 'description')