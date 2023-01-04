import bcrypt
from django.db import models

from common.models import CreatedAtUpdatedAt
from .utils import is_email_validate


class User(CreatedAtUpdatedAt):
    email = models.EmailField(max_length=255, db_index=True, null=True, verbose_name='이메일')
    password_hash = models.CharField(max_length=255, blank=True, null=True, verbose_name='비밀번호 해쉬값')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    class Meta:
        db_table = 'user'
        verbose_name = "수정 일시"

    @staticmethod
    def create_user(email, password):
        is_user_created = False
        if not email or not password:
            return is_user_created

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = dict(email=email, password_hash=password_hash)
        User.objects.create(**user_data)
        return is_user_created

    @staticmethod
    def check_user_validation(insert_email, insert_password):
        is_authenticated = False
        if not insert_email or not insert_password:
            return is_authenticated

        is_email_valid = is_email_validate(insert_email)
        if not is_email_valid:
            return is_authenticated

        password_hash_qs = User.objects.filter(email=insert_email).values('id', 'password_hash')
        if not password_hash_qs:
            return is_authenticated

        password_hash = password_hash_qs.first().get('password_hash')
        user_id = password_hash_qs.first().get('id')
        is_authenticated = bcrypt.checkpw(insert_password.decode('utf-8'), password_hash)
        return is_authenticated, user_id
