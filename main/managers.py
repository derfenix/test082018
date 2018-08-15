from django.db.models import QuerySet, Manager
from django.db.models.manager import BaseManager
from django.utils import timezone


class CommentQuerySet(QuerySet):
    def delete(self):
        self.update(deleted=timezone.now())


class CommentManager(BaseManager.from_queryset(CommentQuerySet)):
    def get_deleted(self):
        return super().get_queryset().filter(deleted__isnull=False)

    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)
