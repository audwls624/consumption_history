import json
from django.views.generic import View
from django.http import JsonResponse
from django.utils import timezone
from django.core.cache import cache

from common import constants
from user.models import User
from user.decorators import login_required
from .models import HouseholdAccount
from .utils import get_account_short_url


class HouseholdAccountDetailView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        result = dict()

        if not account_id:
            result.update(message=constants.API_STATUS_MESSAGE_NOT_FOUND)
            return JsonResponse(result, status=constants.API_STATUS_CODE_NOT_FOUND)

        account_history_details = HouseholdAccount.get_account_history_details(account_id)
        result.update(data=account_history_details, message=constants.API_STATUS_MESSAGE_OK)
        return JsonResponse(result, status=constants.API_STATUS_CODE_OK)

    @login_required
    def post(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        used_amount = request.POST.get('used_amount')
        history = request.POST.get('history')
        is_updated = False
        result = dict()

        if not account_id:
            result.update(message=constants.API_STATUS_MESSAGE_NOT_FOUND)
            return JsonResponse(result, status=constants.API_STATUS_CODE_NOT_FOUND)

        if not used_amount or not history:
            result.update(message=constants.API_STATUS_MESSAGE_NO_CONTENTS)
            return JsonResponse(result, status=constants.API_STATUS_MESSAGE_BAD_REQUEST)

        update_data = dict(id=account_id, used_amount=used_amount, history=history)
        is_updated = HouseholdAccount.update_data(update_data)
        if not is_updated:
            result.update(message=constants.API_STATUS_MESSAGE_INSERT_FAIL)
            return JsonResponse(result, status=constants.API_STATUS_CODE_SERVER_ERROR)

        result.update(message=constants.API_STATUS_MESSAGE_OK)
        return JsonResponse(result, status=constants.API_STATUS_CODE_CREATED)

    @login_required
    def delete(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        is_deleted = False
        result = dict()

        if not account_id:
            result.update(message=constants.API_STATUS_MESSAGE_NOT_FOUND)
            return JsonResponse(result, status=constants.API_STATUS_CODE_NOT_FOUND)

        is_deleted = HouseholdAccount.delete_data(account_id)
        if not is_deleted:
            result.update(message=constants.API_STATUS_MESSAGE_DELETE_FAIL)
            return JsonResponse(result, status=constants.API_STATUS_CODE_SERVER_ERROR)

        result.update(message=constants.API_STATUS_MESSAGE_OK)
        return JsonResponse(result, status=constants.API_STATUS_CODE_OK)


class HouseholdAccountView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        result = dict()
        result.update(message=constants.API_STATUS_MESSAGE_OK)
        return JsonResponse(result, status=constants.API_STATUS_CODE_OK)

    @login_required
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        used_amount = request.POST.get('used_amount')
        history = request.POST.get('history')
        is_success = False
        result = dict()

        if not used_amount or not history:
            result.update(message=constants.API_STATUS_MESSAGE_BAD_REQUEST)
            return JsonResponse(result, status=constants.API_STATUS_MESSAGE_BAD_REQUEST)

        insert_data = dict(user_id=user_id, history=history, used_amount=used_amount)
        is_success = HouseholdAccount.insert_account_data(insert_data)
        if not is_success:
            result.update(message=constants.API_STATUS_MESSAGE_INSERT_FAIL)
            return JsonResponse(result, status=constants.API_STATUS_CODE_SERVER_ERROR)

        result.update(message=constants.API_STATUS_MESSAGE_OK)
        return JsonResponse(result, status=constants.API_STATUS_CODE_CREATED)


class AccountGenerateShorUrlView(View):
    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        http_host = request.META.get('HTTP_HOST')
        result = dict()

        if not account_id:
            result.update(message=constants.API_STATUS_MESSAGE_NOT_FOUND)
            return JsonResponse(result, status=constants.API_STATUS_CODE_NOT_FOUND)

        share_short_url = get_account_short_url(http_host, account_id)
        data = dict(share_short_url=share_short_url)
        result.update(data=data, message=constants.API_STATUS_MESSAGE_OK)
        return JsonResponse(result, status=constants.API_STATUS_CODE_CREATED)
