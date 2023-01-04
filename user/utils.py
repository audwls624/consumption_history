import string
import random

from django.core.validators import validate_email, ValidationError


def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def is_email_validate(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True
