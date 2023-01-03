import jwt
from django.http import JsonResponse
from common.constants import API_STATUS_MESSAGE_EXPIRED_TOKEN, API_STATUS_MESSAGE_INVALID_SIGNATURE, API_STATUS_CODE_UNAUTHORIZED, API_STATUS_MESSAGE_COMMON_TOKEN_ERROR


def decode_jwt(token, secret, algorithms='HS256'):
    try:
        decoded_jwt = jwt.decode(token, secret, algorithms=algorithms)
        return decoded_jwt
    except jwt.exceptions.ExpiredSignatureError:
        return JsonResponse({"message": API_STATUS_MESSAGE_EXPIRED_TOKEN}, status=API_STATUS_CODE_UNAUTHORIZED)
    except jwt.exceptions.InvalidSignatureError:
        return JsonResponse({"message": API_STATUS_MESSAGE_INVALID_SIGNATURE}, status=API_STATUS_CODE_UNAUTHORIZED)
    except Exception as e:
        return JsonResponse({"message": API_STATUS_MESSAGE_COMMON_TOKEN_ERROR}, status=API_STATUS_CODE_UNAUTHORIZED)
