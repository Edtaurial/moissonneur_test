from rest_framework import serializers
from django.contrib.auth.models import User
from moissonneur.models import JeuDeDonnees

class JeuDeDonneesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JeuDeDonnees
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # On ajoute le champ password en 'write_only' pour qu'il ne soit jamais renvoyé en lecture
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        # On utilise create_user pour gérer le hachage du mot de passe
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    # --- AJOUT IMPORTANT POUR LA SECTION 3.3 ---
    def update(self, instance, validated_data):
        # On extrait le mot de passe s'il est présent
        password = validated_data.pop('password', None)
        
        # On met à jour les autres champs normalement
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Si un mot de passe a été fourni, on le hache avec set_password()
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance