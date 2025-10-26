from django.shortcuts import render
from moissonneur.models import JeuDeDonnees
from django.db.models import Count
from django.db.models.functions import TruncMonth

# Create your views here.

def page_statistiques(request):
    # 1. Nombre total de jeux de données
    total_jeux = JeuDeDonnees.objects.count()

    # 2. Répartition par catalogue source
    repartition_par_source = (
        JeuDeDonnees.objects.values('source_catalogue')
        .annotate(total=Count('source_catalogue'))
        .order_by('-total')
    )

    # 3. Les 5 jeux de données les plus récemment modifiés
    jeux_recents = JeuDeDonnees.objects.order_by('-date_modification_source')[:5]

    # 4. Répartition thématique
    repartition_par_organisation = (
        JeuDeDonnees.objects.exclude(organisation__isnull=True).exclude(organisation__exact='')
        .values('organisation')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # 5. Tendance mensuelle basée sur la date d'ajout sur la plateforme
    tendance_qs = (
        JeuDeDonnees.objects.annotate(mois=TruncMonth('date_ajout_plateforme'))
        .values('mois')
        .annotate(total=Count('id'))
        .order_by('mois')
    )
    # On transforme en structure simple pour le template
    tendance_mensuelle = [
        {"label": (row['mois'].strftime('%Y-%m') if row['mois'] else ''), "total": row['total']}
        for row in tendance_qs
    ]

    return render(
        request,
        'tableau_de_bord/statistiques.html',
        {
            "total_jeux": total_jeux,
            "repartition_par_source": repartition_par_source,
            "jeux_recents": jeux_recents,
            "repartition_par_organisation": repartition_par_organisation,
            "tendance_mensuelle": tendance_mensuelle,
        },
    )


from django.contrib.auth.models import User
from django.http import HttpResponse

def creer_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superutilisateur créé !")
    return HttpResponse("Le superutilisateur existe déjà.")

