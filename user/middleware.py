from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from .jwt_utils import get_jwt_user
from common import constants


class JWTMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.headers.get('Authorization'):
            request.user, request.jwt_error_code, request.jwt_token = get_jwt_user(request)
            if request.user == AnonymousUser():
                # 엑세스 토큰 에러
                if request.jwt_error_code:
                    return JsonResponse(dict(message=request.jwt_error_code), status=constants.API_STATUS_CODE_FORBIDDEN)
        else:
            # 비 로그인
            request.user, request.jwt_error_code, request.jwt_token = AnonymousUser(), False, None

        response = self.get_response(request)
        return response
