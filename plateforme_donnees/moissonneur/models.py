from django.db import models

class JeuDeDonnees(models.Model):

    titre = models.CharField(max_length=1024, verbose_name="Titre du jeu de données")
    description = models.TextField(blank=True, null=True, verbose_name="Description")


    source_catalogue = models.CharField(max_length=100, verbose_name="Catalogue source")
    id_source = models.CharField(max_length=255, unique=True, verbose_name="ID sur la source")
    url_source = models.URLField(max_length=500, verbose_name="URL sur la source")
    organisation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Organisation")


    date_creation_source = models.DateTimeField(blank=True, null=True, verbose_name="Date de création (source)")
    date_modification_source = models.DateTimeField(blank=True, null=True, verbose_name="Date de modification (source)")


    date_ajout_plateforme = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout (plateforme)")
    date_maj_plateforme = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour (plateforme)")

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Jeu de Données"
        verbose_name_plural = "Jeux de Données"
