from django.db import models
from django.utils import timezone


class CreatedAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='생성 일시')

    class Meta:
        abstract = True
        verbose_name = "생성 일시"


class UpdatedAt(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='수정 일시')

    class Meta:
        abstract = True
        verbose_name = "수정 일시"


class CreatedAtUpdatedAt(CreatedAt, UpdatedAt):
    class Meta:
        abstract = True

    def insert_data(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError()
            setattr(self, key, value)

        option = dict(force_insert=True)
        self.save(**option)

    def update_data(self, **kwargs):
        update_fields = list()

        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise ValueError()
            if getattr(self, key) != value:
                setattr(self, key, value)
                update_fields.append(key)

        if len(update_fields) > 0:
            update_fields.append('updated_at')
            option = dict(update_fields=update_fields)
            self.save(**option)


class DeletedAt(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='삭제 일시')
    is_deleted = models.BooleanField(db_index=True, default=False, verbose_name='삭제 여부')

    def update_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
        verbose_name = "삭제 일시"
