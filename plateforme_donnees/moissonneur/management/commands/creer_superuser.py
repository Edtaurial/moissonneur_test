import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée un superutilisateur automatiquement s\'il n\'en existe pas.'

    def handle(self, *args, **options):
        # récupérer les informations depuis les variables d'environnement
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'password')

        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Création du superutilisateur '{username}'..."))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé avec succès !"))
        else:
            self.stdout.write(self.style.NOTICE(f"Le superutilisateur '{username}' existe déjà."))

