from django.views.generic import View
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from django.core.cache import cache
from common import constants


class ShortUrlRedirectView(View):
    def get(self, request, *args, **kwargs):
        short_url_key = kwargs.get('short_url_key')
        result = dict()
        if not short_url_key:
            result.update(message=constants.API_STATUS_MESSAGE_NOT_FOUND)
            return JsonResponse(result, status=constants.API_STATUS_CODE_NOT_FOUND)

        cache_key = constants.CACHE_KEY_ACCOUNT_SHORT_URL_MAPPING(random_string=short_url_key)
        account_id = cache.get(cache_key, None)
        if not account_id:
            result.update(message=constants.API_STATUS_MESSAGE_SHORT_URL_EXPIRED)
            return JsonResponse(result, status=constants.API_STATUS_CODE_NOT_FOUND)

        return redirect(reverse('record:account_detail', kwargs=dict(account_id=account_id)))
