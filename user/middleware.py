from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from django.http import JsonResponse
from consumption_history import settings
from .jwt_utils import decode_jwt, get_jwt_user
from common import constants


class JWTMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.headers.get('AUTHORIZATION'):
            request.user, request.jwt_error_code, request.jwt_token = SimpleLazyObject(lambda: get_jwt_user(request))
            if request.api_user.is_anonymous:
                # 엑세스 토큰 에러
                if request.jwt_error_code:
                    return JsonResponse(dict(message=request.jwt_error_code), status=constants.API_STATUS_CODE_FORBIDDEN)
        else:
            # 비 로그인
            request.user, request.jwt_error_code, request.jwt_token = AnonymousUser(), False, None

        response = self.get_response(request)
        return response
