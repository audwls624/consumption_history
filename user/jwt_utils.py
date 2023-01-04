import jwt
from datetime import timedelta
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.utils import timezone

from common.constants import API_STATUS_MESSAGE_EXPIRED_TOKEN, API_STATUS_MESSAGE_INVALID_SIGNATURE, \
    API_STATUS_MESSAGE_COMMON_TOKEN_ERROR, ACCESS_TOKEN_DURAION, REFRESH_TOKEN_DURAION, \
    CACHE_DURATION_REFRESH_TOKEN_MAPPING, CACHE_KEY_REFRESH_TOKEN_MAPPING, TOKEN_TYPE_REFRESH, TOKEN_TYPE_ACCESS, API_STATUS_MESSAGE_TOKEN_TYPE_ERROR, API_STATUS_MESSAGE_TOKEN_PAYLOAD_DATA_ERROR, API_STATUS_MESSAGE_TOKEN_USER_NOT_EXISTS
from consumption_history import settings
from user.models import User
from .utils import get_random_string


def generate_jwt(data, expire_date):
    if not data or not expire_date:
        return ''

    payload = dict(data=data, exp=expire_date)
    encoded_token = jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_token


def get_access_token(user_id):
    if not user_id:
        return ''

    access_token_payload = dict(user_id=user_id, token_type=TOKEN_TYPE_ACCESS)
    access_token_expire_date = timezone.now() + timedelta(seconds=ACCESS_TOKEN_DURAION)
    access_token = generate_jwt(access_token_payload, access_token_expire_date)
    return access_token


def get_refresh_token(user_id):
    if not user_id:
        return ''

    key_string = get_random_string(5)
    refresh_token_payload = dict(key_string=key_string, token_type=TOKEN_TYPE_REFRESH)
    refresh_token_expire_date = timezone.now() + timedelta(seconds=REFRESH_TOKEN_DURAION)
    cache_key = CACHE_KEY_REFRESH_TOKEN_MAPPING.format(random_string=key_string)
    cache.set(cache_key, user_id, CACHE_DURATION_REFRESH_TOKEN_MAPPING)
    refresh_token = generate_jwt(refresh_token_payload, refresh_token_expire_date)
    return refresh_token


def decode_jwt(token):
    try:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        return decoded_jwt, True
    except jwt.exceptions.ExpiredSignatureError:
        return False, API_STATUS_MESSAGE_EXPIRED_TOKEN
    except jwt.exceptions.InvalidSignatureError:
        return False, API_STATUS_MESSAGE_INVALID_SIGNATURE
    except Exception as e:
        return False, API_STATUS_MESSAGE_COMMON_TOKEN_ERROR


def get_jwt_user(request):
    if not request:
        return AnonymousUser(), False, None

    jwt_token = request.headers.get('Authorization')
    if not jwt_token:
        return AnonymousUser(), False, None

    decoded_jwt, error_msg = decode_jwt(jwt_token)
    if not decoded_jwt:
        return AnonymousUser(), error_msg, None

    token_data = decoded_jwt.get('data')
    if not token_data:
        return AnonymousUser(), API_STATUS_MESSAGE_COMMON_TOKEN_ERROR, None

    token_type = token_data.get('token_type')
    if token_type not in (TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH):
        return AnonymousUser(), API_STATUS_MESSAGE_TOKEN_TYPE_ERROR, None

    if token_type == TOKEN_TYPE_REFRESH:
        return AnonymousUser(), False, decoded_jwt

    user_id = token_data.get('user_id')
    if not user_id:
        return AnonymousUser(), API_STATUS_MESSAGE_TOKEN_PAYLOAD_DATA_ERROR, decode_jwt

    try:
        user_obj = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser(), API_STATUS_MESSAGE_TOKEN_USER_NOT_EXISTS, decoded_jwt
    except Exception as e:
        return AnonymousUser(), API_STATUS_MESSAGE_COMMON_TOKEN_ERROR, decoded_jwt
    return user_obj, False, decoded_jwt
