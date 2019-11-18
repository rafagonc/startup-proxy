import dateparser
import pendulum
import datetime
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.utils.timezone import now

from startup.forms_helper import (form_get_view, form_post_error,
                                  form_post_success)
from startup.table_utils import table_response
from startup.proxy.forms import ProxyForm
from startup.proxy.models import Proxy
from startup.proxy.tables import ProxyTable
from startup.proxy.tasks import (check_resources, turn_on_resource, is_ready,
                                 turn_off_all_resources,
                                 turn_off_all_resources)
from startup.proxy.permissions import StaticBasicAuthPermission


class LivenessView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request):
        return render(request,
                      template_name="ok.html",
                      context={
                          "message": "Healthy",
                          "error": False
                      })


class CheckResourcesView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request):
        check_resources()
        return render(request,
                      template_name="ok.html",
                      context={
                          "message": "Healthy",
                          "error": False
                      })


class ProxyIsReadyView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, pk):
        proxy = Proxy.objects.get(pk=pk)
        replicas, ready = is_ready(proxy)
        return Response(
            {
                "replicas": replicas,
                "ready": ready,
                "is_ready": replicas == ready and replicas is not None
            },
            status=200 if replicas == ready and replicas is not None else 502)


class ProxyForceView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request, pk):
        proxy = Proxy.objects.get(pk=pk)
        turn_on_resource(proxy)
        return render(
            request, "loading.html", {
                "name": proxy.name,
                "host": proxy.host,
                "pk": proxy.pk,
                "protocol": "https://" if proxy.https else "http://",
                "error": False
            })


class ProxyView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request):
        host = request.META.get("HTTP_HOST")
        proxies = Proxy.objects.filter(host=host)
        if proxies.count() > 0:
            proxy = proxies.first()
            proxy.last_access_time = pendulum.now("America/Sao_Paulo")
            proxy.save()
            if proxy.should_turn_on() is False and proxy.autostart is False:
                return render(
                    request, "turned_off.html", {
                        "name": proxy.name,
                        "host": proxy.host,
                        "pk": proxy.pk,
                        "start_time": proxy.start_at.strftime("%H:%m"),
                        "end_time": proxy.ends_at.strftime("%H:%m"),
                        "protocol": "https://" if proxy.https else "http://",
                        "error": False
                    })
            else:
                turn_on_resource(proxy)
            return render(
                request, "loading.html", {
                    "name": proxy.name,
                    "host": proxy.host,
                    "pk": proxy.pk,
                    "protocol": "https://" if proxy.https else "http://",
                    "error": False
                })
        else:
            return render(request, "error.html", {
                "message": "No proxies found for host %s" % host,
                "error": True
            })


class ProxyFormview(APIView):
    title = "Create Startup Proxy"
    renderer_classes = (TemplateHTMLRenderer, )

    def post(self, request, pk=None):
        proxy = Proxy() if not pk else Proxy.objects.get(pk=pk)
        form = ProxyForm(request.data, request.FILES, instance=proxy)
        if form.is_valid():
            name = request.data.get("name")
            start_at = request.data.get("start_at")
            ends_at = request.data.get("ends_at")
            service_name = request.data.get("service_name")
            service_port = request.data.get("service_port")
            autostart = request.data.get("autostart") == "on"
            https = request.data.get("https") == "on"
            host = request.data.get("host")
            scale_resource_type = request.data.get("scale_resource_type")
            scale_resource_name = request.data.get("scale_resource_name")
            proxy.name = name
            proxy.last_access_time = now() - datetime.timedelta(hours=4)
            proxy.start_at = dateparser.parse(start_at) if start_at else None
            proxy.ends_at = dateparser.parse(ends_at) if ends_at else None
            proxy.autostart = autostart
            proxy.host = host
            proxy.https = https
            proxy.service_name = service_name
            proxy.service_port = service_port
            proxy.scale_resource_name = scale_resource_name
            proxy.scale_resource_type = scale_resource_type
            proxy.save()
            turn_off_all_resources(filter={"pk": proxy.pk})
            return redirect("/proxy/")
        else:
            return form_post_error(", ".join(form.errors),
                                   request,
                                   pk,
                                   Proxy,
                                   ProxyForm,
                                   title=self.title)

    def get(self, request, pk=None):
        return form_get_view(request=request,
                             pk=pk,
                             model_class=Proxy,
                             form_class=ProxyForm,
                             title=self.title)


class ProxyTableView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request, pk=None):
        if pk:
            try:
                if Proxy.objects.get(pk=pk):
                    Proxy.objects.filter(pk=pk).delete()
            except Exception:
                pass
        return table_response(request,
                              table=ProxyTable(Proxy.objects.all(),
                                               orderable=False),
                              buttons=[{
                                  "name": "Scale down all resources",
                                  "path": "/proxy/suspend/"
                              }])


class TurnOffResourcesView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request):
        turn_off_all_resources()
        return redirect("/proxy/")