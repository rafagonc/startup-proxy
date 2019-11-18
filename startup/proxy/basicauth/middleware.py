from .basicauthutils import validate_request
from .compat import MiddlewareMixin
from .response import HttpResponseUnauthorized


class BasicAuthMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if "proxy" in request.path:
            if not validate_request(request):
                return HttpResponseUnauthorized()
        return None
