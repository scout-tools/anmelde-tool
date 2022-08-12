# myapi/urls.py
from django.urls import include, re_path, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'tag', views.TagViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'message', views.MessageViewSet)
router.register(r'message-type', views.MessageTypeViewSet)
router.register(r'like', views.LikeViewSet)
router.register(r'highscore', views.HighscoreView)
router.register(r'tag-category', views.TagCategoryViewSet)
router.register(r'statistic', views.StatisticView)
router.register(r'material-item', views.MaterialItemViewSet)
router.register(r'material-unit', views.MaterialUnitViewSet)
router.register(r'material-name', views.MaterialNameViewSet)
router.register(r'experiment', views.ExperimentViewSet)
router.register(r'experiment-overview', views.ExperimentOverviewViewSet)
router.register(r'experiment-item', views.ExperimentItemViewSet)
router.register(r'random-event', views.RandomEventViewSet)
router.register(r'top-views', views.TopViewsView)
router.register(r'admin-event', views.AdminEventViewSet)
router.register(r'event-timestamp', views.EventTimestampViewSet)
router.register(r'faq-rating', views.FaqRatingViewSet)
router.register(r'faq', views.FaqViewSet)
router.register(r'image-meta', views.ImageMetaView)
router.register(r'next-best-heimabend', views.NextBestHeimabendViewSet)
router.register(r'event-of-the-week', views.EventOfTheWeekViewSet)
router.register(r'admin-sitemap', views.EventSitemapViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('basic/', include(router.urls)),
    re_path(r'^upload/$', views.ImageView.as_view({'get': 'list'}), name='file-upload'),
    re_path(r'^event-publish/$', views.ChangePublishStatus.as_view(), name='event-publish'),
    re_path(r'^material-items/$', views.MaterialItems.as_view(), name='material-items'),
    re_path(r'^event-item/(?P<event_id>\w+)$', views.EventItem.as_view({'get': 'list'}), name='event-item')
]
