"""
Script d'importation de données CSV dans la base de données
Usage: python import_csv.py <fichier.csv>
"""
import os
import sys
import django
import csv
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plateforme_donnees.settings')
django.setup()

from moissonneur.models import JeuDeDonnees


def parse_datetime(date_str):
    """Parse une date ISO format avec gestion des erreurs"""
    if not date_str or date_str == 'NULL':
        return None
    try:
        # Format ISO: 2025-10-21T13:53:57.008Z
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return None


def import_from_csv(csv_file):
    """Importe les données depuis un fichier CSV"""
    
    if not os.path.exists(csv_file):
        print(f"[ERREUR] Fichier introuvable: {csv_file}")
        return
    
    imported = 0
    updated = 0
    errors = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # Vérifier si l'enregistrement existe déjà
                jeu, created = JeuDeDonnees.objects.update_or_create(
                    id_source=row['id_source'],
                    defaults={
                        'titre': row['titre'],
                        'description': row['description'],
                        'source_catalogue': row['source_catalogue'],
                        'url_source': row['url_source'],
                        'organisation': row['organisation'],
                        'date_creation_source': parse_datetime(row.get('date_creation_source')),
                        'date_modification_source': parse_datetime(row.get('date_modification_source')),
                        'date_ajout_plateforme': parse_datetime(row.get('date_ajout_plateforme')),
                        'date_maj_plateforme': parse_datetime(row.get('date_maj_plateforme')),
                    }
                )
                
                if created:
                    imported += 1
                    print(f"[+] Cree: {jeu.titre[:50]}...")
                else:
                    updated += 1
                    print(f"[*] Mis a jour: {jeu.titre[:50]}...")
                    
            except Exception as e:
                errors += 1
                print(f"[ERROR] Ligne {reader.line_num}: {e}")
                continue
    
    print("\n" + "="*60)
    print(f"[OK] Import termine:")
    print(f"  - Crees: {imported}")
    print(f"  - Mis a jour: {updated}")
    print(f"  - Erreurs: {errors}")
    print("="*60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python import_csv.py <fichier.csv>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    import_from_csv(csv_file)
