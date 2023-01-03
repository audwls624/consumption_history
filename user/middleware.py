from django.core.exceptions import PermissionDenied
from http import HTTPStatus
from django.http import JsonResponse
from consumption_history import settings
from .jwt_utils import decode_jwt


class JWTMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.headers.get('AUTHORIZATION')
        if not jwt_token:
            raise PermissionDenied()

        payload = decode_jwt(jwt_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        user_id = payload.get('user_id')
        if not user_id:
            raise PermissionDenied()

        response = self.get_response(request)
        return response
