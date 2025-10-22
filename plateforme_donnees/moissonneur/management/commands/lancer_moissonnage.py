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

        # --- NOUVELLE LOGIQUE DE PAGINATION ---
        # On compte combien de jeux de cette source on a déjà pour savoir où commencer.
        start_index = JeuDeDonnees.objects.filter(source_catalogue=SOURCE_CATALOGUE).count()
        self.stdout.write(f"  {start_index} jeux de données '{SOURCE_CATALOGUE}' déjà en base. Demande des 100 suivants...")

        # On définit les paramètres de notre requête.
        # 'start' est l'offset, pour récupérer les pages suivantes.
        params = {
            'rows': 100,
            'start': start_index
        }
        # ------------------------------------

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




















# import requests
# import re
# import warnings
# from django.core.management.base import BaseCommand
# from django.utils.dateparse import parse_datetime
# from django.utils import timezone
# from django.db import DatabaseError
# from moissonneur.models import JeuDeDonnees
#
# # L'URL de l'API CKAN pour la recherche de jeux de données (package_search)
# # CORRIGÉ : L'URL est maintenant une chaîne de caractères simple.
# API_URL = "https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search"
# SOURCE_CATALOGUE = "CanWin"
#
#
# class Command(BaseCommand):
#     help = 'Lance le moissonnage des données depuis le catalogue CanWin (avec pagination).'
#
#     def add_arguments(self, parser):
#         parser.add_argument('--rows', type=int, default=100, help='Nombre d\'éléments demandés par page à l\'API (rows).')
#         parser.add_argument('--limit', type=int, default=0, help='Nombre maximal de jeux à traiter (- 0 = sans limite).')
#
#     def handle(self, *args, **options):
#         # Supprimer les warnings RuntimeWarning générés par Django sur les datetimes naïfs
#         warnings.filterwarnings(
#             "ignore",
#             message=r"DateTimeField .* received a naive datetime",
#             category=RuntimeWarning,
#         )
#
#         self.stdout.write(self.style.SUCCESS('--- Début du moissonnage pour CanWin ---'))
#
#         # Récupérer la verbosité (1 par défaut). Si >1, on affiche les messages par-entrée.
#         verbosity = int(options.get('verbosity', 1))
#
#         rows = int(options.get('rows', 100))  # nombre d'éléments par page (ajuster selon besoin)
#         limit = int(options.get('limit', 0))  # 0 => pas de limite
#         start = 0
#         total = None
#         compteur_creation = 0
#         compteur_maj = 0
#         compteur_erreurs_db = 0
#         traites = 0
#
#         def make_aware(dt):
#             """Transforme un datetime naive en aware en supposant UTC si nécessaire."""
#             if not dt:
#                 return None
#             if timezone.is_naive(dt):
#                 # on suppose que les timestamps fournis par l'API sont en UTC
#                 try:
#                     return timezone.make_aware(dt, timezone.utc)
#                 except Exception:
#                     # fallback sur la timezone par défaut de Django
#                     return timezone.make_aware(dt, timezone.get_default_timezone())
#             return dt
#
#         def remove_4byte_chars(s: str) -> str:
#             # supprime les caractères dont le point de code est > 0xFFFF (emoji, etc.)
#             if s is None:
#                 return s
#             return ''.join(ch for ch in s if ord(ch) <= 0xFFFF)
#
#         def sanitize_text(value, field_name=None):
#             if value is None:
#                 return None
#             if not isinstance(value, str):
#                 value = str(value)
#             # enlever les caractères 4-byte problématiques
#             value = remove_4byte_chars(value)
#             # tronquer si le champ a une limite (CharField)
#             if field_name:
#                 try:
#                     field = JeuDeDonnees._meta.get_field(field_name)
#                     max_len = getattr(field, 'max_length', None)
#                     if max_len:
#                         return value[:max_len]
#                 except Exception:
#                     pass
#             return value
#
#         try:
#             while True:
#                 params = {"rows": rows, "start": start}
#                 response = requests.get(API_URL, params=params)
#                 response.raise_for_status()
#                 data = response.json()
#
#                 if not data.get("success"):
#                     self.stdout.write(self.style.ERROR("L'API a retourné une erreur."))
#                     break
#
#                 result = data.get("result", {})
#                 if total is None:
#                     total = result.get("count", 0)
#
#                 jeux_de_donnees = result.get("results", [])
#                 if not jeux_de_donnees:
#                     break
#
#                 for item in jeux_de_donnees:
#                     # normaliser id_source
#                     id_src = (item.get("id") or "").strip()
#                     if not id_src:
#                         continue
#
#                     # parser et rendre aware les dates si présentes
#                     date_creation = make_aware(parse_datetime(item.get("metadata_created"))) if item.get("metadata_created") else None
#                     date_modification = make_aware(parse_datetime(item.get("metadata_modified"))) if item.get("metadata_modified") else None
#
#                     # sanitize/trim champs potentiellement problématiques
#                     titre = sanitize_text(item.get("title", "Titre non disponible"), field_name='titre')
#                     description = sanitize_text(item.get("notes", ""), field_name='description')
#                     organisation = sanitize_text((item.get("organization") or {}).get("title", "Organisation non spécifiée")) if item.get("organization") else "Organisation non spécifiée"
#                     url_source = sanitize_text(f"https://canwin-datahub.ad.umanitoba.ca/dataset/{item.get('name')}")
#
#                     try:
#                         jeu, created = JeuDeDonnees.objects.update_or_create(
#                             id_source=id_src,
#                             defaults={
#                                 "titre": titre,
#                                 "description": description,
#                                 "source_catalogue": SOURCE_CATALOGUE,
#                                 "url_source": url_source,
#                                 "organisation": organisation,
#                                 "date_creation_source": date_creation,
#                                 "date_modification_source": date_modification,
#                             },
#                         )
#
#                         if created:
#                             compteur_creation += 1
#                             if verbosity > 1:
#                                 self.stdout.write(f"  [CRÉÉ] {jeu.titre}")
#                         else:
#                             compteur_maj += 1
#                             if verbosity > 1:
#                                 self.stdout.write(f"  [MIS À JOUR] {jeu.titre}")
#
#                     except DatabaseError as e:
#                         # ignorer l'enregistrement problématique mais compter les erreurs
#                         compteur_erreurs_db += 1
#                         if verbosity > 0:
#                             self.stdout.write(self.style.WARNING(f"Erreur DB sur id_source={id_src}: {e}"))
#                         continue
#                     except Exception as e:
#                         # catch any other unexpected exception to avoid stopping the whole run
#                         compteur_erreurs_db += 1
#                         if verbosity > 0:
#                             self.stdout.write(self.style.WARNING(f"Erreur inattendue sur id_source={id_src}: {e}"))
#                         continue
#
#                     traites += 1
#                     if limit and traites >= limit:
#                         break
#
#                 if limit and traites >= limit:
#                     break
#
#                 start += rows
#                 if start >= total:
#                     break
#
#             self.stdout.write(self.style.SUCCESS('--- Moissonnage terminé ---'))
#             self.stdout.write(f'{compteur_creation} jeux de données créés.')
#             self.stdout.write(f'{compteur_maj} jeux de données mis à jour.')
#             if compteur_erreurs_db:
#                 self.stdout.write(self.style.WARNING(f'{compteur_erreurs_db} enregistrements ignorés à cause d\'erreurs.'))
#
#         except requests.exceptions.RequestException as e:
#             self.stdout.write(self.style.ERROR(f'Erreur de connexion à l\'API : {e}'))