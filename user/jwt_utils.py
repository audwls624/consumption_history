import jwt

from django.conf import settings
from django.contrib.auth.models import AnonymousUser


def parsing_jwt(token, secret, algorithms='HS256'):
    try:
        decoded_jwt = jwt.decode(token, secret, algorithms=algorithms)
        return decoded_jwt
    except jwt.exceptions.ExpiredSignatureError:
        return
    except jwt.exceptions.InvalidSignatureError:
        return
    except Exception as e:
        return
