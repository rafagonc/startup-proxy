from rest_framework.response import Response
from rest_framework.validators import ValidationError


def success(boolean, status=200):
    return Response({"success": boolean}, status)


def response(obj, status=200):
    return Response({"success": True, "content": obj}, status)


def response_paginator(count, paginator, data, status=200):
    return response({
        "count": count,
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
        "results": data
    })


def error_response(obj, status=400):
    return Response({"success": False, "error": obj}, status)


def error_response_with_obj(obj, err, status=400):
    return Response({"success": False, "error": err, "content": obj}, status)


def get_field(request, field, default=None, optional=False):
    value = request.data.get(field)
    if value is None and optional is False:
        raise ValidationError("missing field " + field)
    if value is None:
        return default
    return value
