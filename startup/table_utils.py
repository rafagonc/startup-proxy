from django_tables2 import columns
from django.utils.html import format_html
from django.shortcuts import render


def table_response(request, table, buttons):
    return render(request, 'tables.html', {"table": table, "buttons": buttons})


class DeleteColumn(columns.Column):
    def __init__(self, app_name, model_name, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        super(DeleteColumn, self).__init__(accessor="pk", *args, **kwargs)

    def render(self, value):
        return format_html(
            "<a href='/proxy/%s/delete/'><button class='btn btn-danger'>Delete</button></a>"
            % (value))


class ButtonColumn(columns.Column):
    def __init__(self, title, path, *args, **kwargs):
        self.title = title
        self.path = path
        super(ButtonColumn, self).__init__(accessor="pk", *args, **kwargs)

    def render(self, value):
        return format_html(
            "<a href='%s'><button class='btn btn-dark'>%s</button></a>" %
            (self.path % value, self.title))
