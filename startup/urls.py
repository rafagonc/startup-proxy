from django.conf.urls import url
from django.conf.urls.static import static
from startup import settings
from startup.metrics import views as metric_views
from startup.proxy import views as proxy_views

urlpatterns = [
    url(r'metrics', metric_views.MetricsView.as_view()),
    url(r'^status/$', proxy_views.LivenessView.as_view()),
    url(r'^check/$', proxy_views.CheckResourcesView.as_view()),
    url(r'^ready/(?P<pk>(\d+))/$', proxy_views.ProxyIsReadyView.as_view()),
    url(r'^proxy/suspend/$', proxy_views.TurnOffResourcesView.as_view()),
    url(r'^proxy/$', proxy_views.ProxyTableView.as_view()),
    url(r'^proxy/(?P<pk>(\d+))/force/', proxy_views.ProxyForceView.as_view()),
    url(r'^proxy/create/$', proxy_views.ProxyFormview.as_view()),
    url(r'^proxy/edit/$', proxy_views.ProxyFormview.as_view()),
    url(r'^proxy/(?P<pk>(\d+))/edit/$', proxy_views.ProxyFormview.as_view()),
    url(r'^proxy/(?P<pk>(\d+))/delete/$',
        proxy_views.ProxyTableView.as_view()),
    url(r'^$', proxy_views.ProxyView.as_view()),
    url(r'.*', proxy_views.ProxyView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
