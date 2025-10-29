from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .schema import schema
from .views import PrivateGraphQLView


graphql_view = csrf_exempt(PrivateGraphQLView.as_view(graphiql=True, schema=schema))

urlpatterns = [
    path("gql/", graphql_view, name="graphql"),
]
