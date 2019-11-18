from django_tables2.tables import Table
from django_tables2.columns import Column
from startup.proxy.models import Proxy
from startup.table_utils import ButtonColumn, DeleteColumn


class ProxyTable(Table):
    scale_resource_type = Column(verbose_name="Resource Type")
    scale_resource_name = Column(verbose_name="Resource Name")
    autostart = Column(verbose_name="Autostart")
    edit = ButtonColumn(verbose_name="Edit",
                        title="Edit",
                        path="/proxy/%s/edit/")
    delete = DeleteColumn("startup", "Proxy", verbose_name="Delete")

    class Meta:
        model = Proxy
        template = 'django_tables2/bootstrap-responsive.html'