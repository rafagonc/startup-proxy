from rest_framework import permissions
from startup.proxy.basicauth.basicauthutils import validate_request
from startup.proxy.basicauth.response import HttpResponseUnauthorized


class StaticBasicAuthPermission(permissions.BasePermission):
    message = 'Static basic auth permission.'

    def has_permission(self, request, view):
        import ipdb
        ipdb.set_trace()
        if not validate_request(request):
            return HttpResponseUnauthorized()
        else:
            return True