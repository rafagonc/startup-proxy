from django.forms import (ModelForm, CharField, ChoiceField, IntegerField)
from .models import Proxy


class ProxyForm(ModelForm):
    scale_resource_name = CharField(required=True,
                                    label="Resource Name",
                                    help_text="Ex: jenkins-jenkins")
    scale_resource_type = ChoiceField(required=True,
                                      label="Resource Type. Ex: deployment",
                                      choices=Proxy.RESOURCE_TYPES)
    host = CharField(required=True,
                     label="Host",
                     help_text="Ex: subdomain.domain.com")
    duration_threshold = IntegerField(required=False,
                                      label="Duration Threshold",
                                      help_text="Duration After Cold Start")
    start_at = CharField(required=False,
                         label="Starts At",
                         help_text="UTC - HH:MM")
    ends_at = CharField(required=False,
                        label="Ends At",
                        help_text="UTC - HH:MM")

    class Meta:
        model = Proxy
        fields = [
            'name', 'host', 'scale_resource_name', 'scale_resource_type',
            'service_name', 'service_port', 'autostart', 'duration_threshold',
            'start_at', 'ends_at', 'https'
        ]
        excludes = ["resource_on", "suspend"]
