from django.db import models
from common.models import CreatedAtUpdatedAt, DeletedAt
from user.models import User


class HouseholdAccount(CreatedAtUpdatedAt, DeletedAt):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='house_hold_accounts', verbose_name='유저 ID')
    used_amount = models.BigIntegerField(default=0, verbose_name='금액')
    history = models.CharField(max_length=255, blank=True, null=True, verbose_name='사용 내')

    class Meta:
        db_table = 'household_account'
        verbose_name = '가계부 기록'

    @classmethod
    def insert_account_data(cls, data):
        if not data:
            return False

        try:
            cls.objects.create(**data)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def delete_data(cls, id):
        if not id:
            return False
        try:
            cls.objects.filter(id=id).update(is_deleted=True)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def update_data(cls, data):
        if not data:
            return False
        try:
            cls.objects.update(**data)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def get_user_account_history_list(cls, user_id):
        account_history_list = list
        if not user_id:
            return account_history_list

        account_history_list = cls.objects.filter(user_id=user_id, is_deleted=False).values('used_amount', 'history')
        return list(account_history_list)

    @classmethod
    def get_account_history_details(cls, account_id):
        get_account_history_details = dict()
        if not account_id:
            return get_account_history_details

        account_history_qs = cls.objects.filter(id=account_id).values('id', 'user_id', 'used_amount', 'history')
        if not account_history_qs:
            return get_account_history_details

        get_account_history_details = account_history_qs.first()
        return get_account_history_details





