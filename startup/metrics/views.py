import prometheus_client
from django.http import HttpResponse
from django.views import View


def generate_application_level_metrics():
    pass


class MetricsView(View):
    def get(self, request, *args, **kwargs):
        generate_application_level_metrics()
        metrics_page = prometheus_client.generate_latest()
        return HttpResponse(metrics_page,
                            content_type=prometheus_client.CONTENT_TYPE_LATEST)
