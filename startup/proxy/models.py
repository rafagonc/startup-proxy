import pendulum
from django.utils.timezone import now
from django.db.models import (BooleanField, CharField, DateTimeField,
                              IntegerField, Model, TimeField)


class Proxy(Model):

    RESOURCE_TYPES = (("deployment", "deployment"), )

    name = CharField(max_length=255)
    scale_resource_name = CharField(max_length=255)
    scale_resource_type = CharField(max_length=255, choices=RESOURCE_TYPES)
    host = CharField(max_length=255)
    start_at = TimeField(null=True)
    ends_at = TimeField(null=True)
    last_access_time = DateTimeField(null=True)
    autostart = BooleanField(default=False)
    is_on = BooleanField(default=True)
    duration_threshold = IntegerField(default=60)
    replicas = IntegerField(default=1)
    service_name = CharField(max_length=255, null=True)
    service_port = IntegerField(null=True)
    https = BooleanField(default=True)

    def should_turn_on(self):
        if self.start_at is None or self.ends_at is None:
            return True
        date_start = pendulum.now().replace(hour=self.start_at.hour,
                                            minute=self.start_at.minute)
        date_end = pendulum.now().replace(hour=self.ends_at.hour,
                                          minute=self.ends_at.minute)
        period = pendulum.Period(date_start, date_end)
        return now() in period

    def to_dict(self):
        return {
            "name": self.name,
            "scale_resource_name": self.scale_resource_name,
            "scale_resource_type": self.scale_resource_type,
            "start_at": self.start_at,
            "ends_at": self.ends_at,
            "duration_threshold": self.duration_threshold,
            "host": self.host,
            "https": self.https,
            "is_on": self.is_on,
            "service_name": self.service_name,
            "service_port": self.service_port,
            "autostart": self.autostart
        }
