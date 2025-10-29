from django.shortcuts import render


from graphene_django.views import GraphQLView
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponseForbidden


class PrivateGraphQLView(GraphQLView):

    def dispatch(self, request, *args, **kwargs):

        auth = TokenAuthentication()
        try:

            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple:

                request.user = user_auth_tuple[0]  # Si l'authentification reussit, on attache l'utilisateur a la requete
            else:
                # on refuse l'acces sinon
                 return HttpResponseForbidden("Authentification requise.")

        except AuthenticationFailed as e:
            # Si l'authentification échoue pour des raisons de jeton invalide ou manquan t on refuse l'acces
            return HttpResponseForbidden(f"Authentification échouée: {e}")

        # si l'authentification a réussi, on retourne la vue
        return super().dispatch(request, *args, **kwargs)

