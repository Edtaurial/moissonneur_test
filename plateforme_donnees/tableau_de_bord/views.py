from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncYear
from moissonneur.models import JeuDeDonnees


def page_statistiques(request):
    # nombre total de jeux de donnees
    total_jeux = JeuDeDonnees.objects.count()

    # rpartition par catalogue source
    repartition_par_source = JeuDeDonnees.objects.values('source_catalogue').annotate(
        total=Count('source_catalogue')).order_by('-total')

    # les 5 jeux de donnees les plus recemment modifies
    jeux_recents = JeuDeDonnees.objects.order_by('-date_modification_source')[:5]

    # repartition par organisation

    repartition_par_organisation = JeuDeDonnees.objects \
        .values('organisation') \
        .annotate(total=Count('organisation')) \
        .order_by('-total')[:10]  # Top 10

    # Tendances Temporelles simples (par annee de creation)
    tendances_temporelles = JeuDeDonnees.objects.annotate(
        annee_creation=TruncYear('date_creation_source')
    ).values('annee_creation') \
        .annotate(total=Count('id')) \
        .order_by('annee_creation')


    context = {
        'total_jeux': total_jeux,
        'repartition_par_source': repartition_par_source,
        'jeux_recents': jeux_recents,
        'repartition_par_organisation': repartition_par_organisation,
        'tendances_temporelles': tendances_temporelles,
    }

    return render(request, 'tableau_de_bord/statistiques.html', context)

#creation dun superutilisateur pour l'administration
from django.contrib.auth.models import User
from django.http import HttpResponse

def creer_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superutilisateur créé !")
    return HttpResponse("Le superutilisateur existe déjà.")
