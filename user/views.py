from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone
from django.core.cache import cache

from common import constants
from .models import User
from .jwt_utils import get_access_token, get_refresh_token, decode_jwt
from .utils import is_email_validate
from .decorators import login_required


class UserSignUpView(View):
    def post(self, request, *args, **kwargs):
        body = request.POST
        request_email = body.get('user_email')
        request_passowrd = body.get('password')
        result = dict()

        if not request_email or not request_passowrd:
            result.update(message=constants.API_STATUS_MESSAGE_BAD_REQUEST)
            return JsonResponse(result, status=constants.API_STATUS_MESSAGE_BAD_REQUEST)

        is_email_valid = is_email_validate(request_email)
        if not is_email_valid:
            result.update(message=constants.API_STATUS_MESSAGE_EMAIL_VALIDATION_FALSE)
            return JsonResponse(result, status=constants.API_STATUS_MESSAGE_BAD_REQUEST)

        try:
            User.create_user(request_email, request_passowrd)
        except Exception as e:
            result.update(message=constants.API_STATUS_MESSAGE_SERVER_ERROR, error_msg=str(e))
            return JsonResponse(result, status=constants.API_STATUS_CODE_SERVER_ERROR)

        return JsonResponse(dict(message=constants.API_STATUS_MESSAGE_OK), status=constants.API_STATUS_CODE_CREATED)


class UserLoginView(View):
    def post(self, request, *args, **kwargs):
        body = request.POST
        request_email = body.get('user_email')
        request_passowrd = body.get('password')
        is_authenticated = False
        result = dict()

        if not request_email or not request_passowrd:
            result.update(message=constants.API_STATUS_MESSAGE_BAD_REQUEST)
            return JsonResponse(result, status=constants.API_STATUS_CODE_BAD_REQUEST)

        is_authenticated, user_id = User.check_user_validation(request_email, request_passowrd)
        if not is_authenticated:
            result.update(message=constants.API_STATUS_MESSAGE_UNAUTHORIZED)
            return JsonResponse(result, status=constants.API_STATUS_CODE_UNAUTHORIZED)

        access_token, refresh_token = get_access_token(user_id), get_refresh_token(user_id)
        result.update(
            message=constants.API_STATUS_MESSAGE_OK,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        return JsonResponse(result, status=constants.API_STATUS_CODE_OK)


# 로그아웃 별도 구현 X
# @login_required
# class UserLogoutView(View):
#     def post(self, request, *args, **kwargs):
#         result = dict()
#         response = JsonResponse(result, status=constants.API_STATUS_CODE_OK)
#         return response


class RefreshTokenView(View):
    def get(self, request, *args, **kwargs):
        refresh_token_data = request.jwt_token.get('data')
        _now = timezone.now()
        result = dict()

        refresh_token_key_string = refresh_token_data.get('key_string')
        if not refresh_token_key_string:
            result.update(message=constants.API_STATUS_MESSAGE_TOKEN_INVALID_KEY_STRING)
            return JsonResponse(result, status=constants.API_STATUS_CODE_FORBIDDEN)

        cache_key = constants.CACHE_KEY_REFRESH_TOKEN_MAPPING.format(random_string=refresh_token_key_string)
        user_id = cache.get(cache_key, None)
        if not user_id:
            result.update(message=constants.API_STATUS_MESSAGE_TOKEN_INVALID_KEY_STRING)
            return JsonResponse(result, status=constants.API_STATUS_CODE_FORBIDDEN)

        access_token = get_access_token(user_id)
        result.update(message=constants.API_STATUS_MESSAGE_OK, access_token=access_token)
        return JsonResponse(result, status=constants.API_STATUS_CODE_OK)
