from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from common import constants


def login_required(original_function):
    def wrapper(self, request, *args, **kwargs):
        if not hasattr(request, 'user') or not hasattr(request, 'jwt_error_code') or not hasattr(request, 'jwt_token'):
            return JsonResponse(dict(message=constants.API_STATUS_MESSAGE_FORBIDDEN), status=constants.API_STATUS_CODE_FORBIDDEN)

        if request.api_user == AnonymousUser():
            return JsonResponse(dict(message=constants.API_STATUS_MESSAGE_UNAUTHORIZED), status=constants.API_STATUS_CODE_UNAUTHORIZED)

        return original_function(self, request, *args, **kwargs)
    return wrapper
