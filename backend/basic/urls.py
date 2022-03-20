# myapi/urls.py
from django.urls import include, path
from rest_framework_nested import routers
# from graphene_django.views import GraphQLView

from . import views

router = routers.SimpleRouter()
router.register(r'scout-hierarchy', views.ScoutHierarchyViewSet)
router.register(r'zip-code', views.ZipCodeViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'tag-types', views.TagTypeViewSet)
router.register(r'attributes', views.AttributeViewSet)

router.register(r'travel-type-choices', views.TravelTypeViewSet, basename='travel-type-choices')
router.register(r'travel-slots-choices', views.TravelSlotsViewSet, basename='travel-slots-choices')
router.register(r'attribute-choices', views.AttributeTypeViewSet, basename='attribute-choices')

router.register(r'faq', views.DescriptionViewSet, basename='faq')
router.register(r'legal', views.DescriptionViewSet, basename='legal')
router.register(r'privacy', views.DescriptionViewSet, basename='privacy')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path("graphql", GraphQLView.as_view(graphiql=True)),
]
