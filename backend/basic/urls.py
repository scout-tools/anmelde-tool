from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'scout-hierarchy', views.ScoutHierarchyViewSet)
router.register(r'scout-hierarchy-detail', views.ScoutHierarchyDetailedViewSet)
router.register(r'zip-code', views.ZipCodeViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'tag-types', views.TagTypeViewSet)
router.register(r'attributes', views.AttributeViewSet)
router.register(r'eat-habits', views.EatHabitViewSet)
router.register(r'theme', views.FrontendThemeViewSet)
router.register(r'message', views.MessageViewSet)
router.register(r'message-type', views.MessageTypeViewSet)

router.register(r'travel-type-choices', views.TravelTypeViewSet, basename='travel-type-choices')
router.register(r'travel-slots-choices', views.TravelSlotsViewSet, basename='travel-slots-choices')
router.register(r'attribute-choices', views.AttributeTypeViewSet, basename='attribute-choices')

router.register(r'faq', views.DescriptionViewSet, basename='faq')
router.register(r'privacy', views.DescriptionViewSet, basename='privacy')

urlpatterns = [
    path('', include(router.urls)),
    # path("graphql", GraphQLView.as_view(graphiql=True)),
]
