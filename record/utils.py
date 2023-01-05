from django.core.cache import cache
from user.utils import get_random_string
from common.constants import CACHE_DURATION_SHORT_URL_DURATION, CACHE_KEY_ACCOUNT_SHORT_URL_MAPPING


def get_account_short_url(http_host, account_id):
    if not account_id or not http_host:
        return ''

    random_string = get_random_string(5)
    short_url = f"{http_host}/c/s/{random_string}"
    cache_key = CACHE_KEY_ACCOUNT_SHORT_URL_MAPPING.format(random_string=random_string)
    cache.set(cache_key, account_id, CACHE_DURATION_SHORT_URL_DURATION)
    return short_url
