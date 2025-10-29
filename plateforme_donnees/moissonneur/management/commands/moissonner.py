import requests
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from moissonneur.models import JeuDeDonnees

API_URL = "https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search"
SOURCE_CATALOGUE = "CanWin"

class Command(BaseCommand):
    help = 'Lance le moissonnage des données depuis le catalogue CanWin.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'--- Début du moissonnage pour {SOURCE_CATALOGUE} (limite 100) ---'))


        start_index = JeuDeDonnees.objects.filter(source_catalogue=SOURCE_CATALOGUE).count()
        self.stdout.write(f"  {start_index} jeux de données '{SOURCE_CATALOGUE}' déjà en base. Demande des 100 suivants...")


        params = {
            'rows': 100,  #100 jeux de donnees par requete
            'start': start_index
        }


        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                jeux_de_donnees = data.get('result', {}).get('results', [])

                if not jeux_de_donnees:
                    self.stdout.write(self.style.WARNING('  Aucun nouveau jeu de données trouvé. Le catalogue est peut-être entièrement moissonné.'))
                    return

                compteur_creation = 0
                compteur_maj = 0

                for item in jeux_de_donnees:
                    jeu, created = JeuDeDonnees.objects.update_or_create(
                        id_source=item.get('id'),
                        defaults={
                            'titre': item.get('title', 'Titre non disponible'),
                            'description': item.get('notes', ''),
                            'source_catalogue': SOURCE_CATALOGUE,
                            'url_source': f"https://canwin-datahub.ad.umanitoba.ca/dataset/ {item.get('name')}",
                            'organisation': item.get('organization', {}).get('title', 'Organisation non spécifiée') if item.get('organization') else 'Organisation non spécifiée',
                            'date_creation_source': parse_datetime(item.get('metadata_created')) if item.get('metadata_created') else None,
                            'date_modification_source': parse_datetime(item.get('metadata_modified')) if item.get('metadata_modified') else None,
                        }
                    )

                    if created:
                        compteur_creation += 1
                    else:
                        compteur_maj += 1

                self.stdout.write(f"  {len(jeux_de_donnees)} jeux de données traités depuis l'API.")
                self.stdout.write(self.style.SUCCESS(f'--- Moissonnage terminé ---'))
                self.stdout.write(f'{compteur_creation} jeux de données créés.')
                self.stdout.write(f'{compteur_maj} jeux de données mis à jour.')


            else:
                self.stdout.write(self.style.ERROR('L\'API a retourné une erreur.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erreur de connexion à l\'API : {e}'))



