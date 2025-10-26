from django.shortcuts import render
from moissonneur.models import JeuDeDonnees
from django.db.models import Count
# Create your views here.
def page_statistiques(request):
    # 1. Nombre total de jeux de données
    total_jeux = JeuDeDonnees.objects.count()

    # 2. Répartition par catalogue source
    #    Ceci va grouper les jeux par 'source_catalogue' et compter combien il y en a dans chaque groupe.
    repartition_par_source = JeuDeDonnees.objects.values('source_catalogue').annotate(total=Count('source_catalogue')).order_by('-total')

    # 3. Les 5 jeux de données les plus récemment modifiés
    jeux_recents = JeuDeDonnees.objects.order_by('-date_modification_source')[:5]


    return render(request, 'tableau_de_bord/statistiques.html', {"total_jeux": total_jeux, "repartition_par_source": repartition_par_source, "jeux_recents": jeux_recents})


from django.contrib.auth.models import User
from django.http import HttpResponse

def creer_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superutilisateur créé !")
    return HttpResponse("Le superutilisateur existe déjà.")
