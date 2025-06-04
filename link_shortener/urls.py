from django.urls import path
from .views import ShortURLCreateView, RedirectView, ShortURLListView, ShortURLDeactivateView, ShortURLStatsView

urlpatterns = [
    path('shorten/', ShortURLCreateView.as_view(), name='shorten'),
    path('links/', ShortURLListView.as_view(), name='links'),
    path('code/<str:short_code>/', RedirectView.as_view(), name='redirect'),
    path('shorten/<str:short_code>/deactivate/', ShortURLDeactivateView.as_view(), name='shorten-deactivate'),
    path('shorten/stats/', ShortURLStatsView.as_view(), name='shorten-stats'),

]
