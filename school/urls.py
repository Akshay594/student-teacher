from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

GraphQLView.graphiql_template = "graphene_graphiql_explorer/graphiql.html"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)