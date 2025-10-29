from django.shortcuts import render
from moissonneur.models import JeuDeDonnees
from django.db.models import Count
from django.db.models.functions import TruncMonth

# Create your views here.

def page_statistiques(request):
    # nombre total de jeux de donnees
    total_jeux = JeuDeDonnees.objects.count()

    #  repartition par catalogue source
    repartition_par_source = (
        JeuDeDonnees.objects.values('source_catalogue')
        .annotate(total=Count('source_catalogue'))
        .order_by('-total')
    )

    # les 5 jeux de donnees les plus recemment modifies
    jeux_recents = JeuDeDonnees.objects.order_by('-date_modification_source')[:5]

    # repartition thematique
    repartition_par_organisation = (
        JeuDeDonnees.objects.exclude(organisation__isnull=True).exclude(organisation__exact='')
        .values('organisation')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # tendance mensuelle basee sur la date d'ajout sur la plateforme
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

# creation d un super utilisateur
def creer_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superutilisateur créé !")
    return HttpResponse("Le superutilisateur existe déjà.")

