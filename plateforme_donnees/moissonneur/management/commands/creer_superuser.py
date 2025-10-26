import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Crée ou met à jour un superutilisateur à partir des variables d'environnement."

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '') # Utilise une chaîne vide si non défini


        if not username or not password:
            self.stdout.write(self.style.NOTICE("Variables DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD non définies. Annulation."))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.NOTICE(f"Le superutilisateur '{username}' existe déjà. Mise à jour du mot de passe..."))
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Mot de passe pour '{username}' mis à jour avec succès."))
        else:
            self.stdout.write(self.style.WARNING(f"Création du superutilisateur '{username}'..."))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé avec succès !"))
