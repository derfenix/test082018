import difflib

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.db.transaction import atomic
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.translation import ugettext as _

from main.managers import CommentManager
from test082018.local_storage import storage

differ = difflib.Differ()


class Comment(models.Model):
    root = models.ForeignKey('self', verbose_name=_('root comment'), related_name='root_children',
                             null=True, blank=True, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', verbose_name=_('parent comment'), related_name='children',
                               null=True, blank=True, on_delete=models.DO_NOTHING)
    level = models.IntegerField(_('comment level'), default=0)

    user_id = models.IntegerField(_('comment\'s author id'), db_index=True)

    target = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField(db_index=True)

    created = models.DateTimeField(_('created'), auto_now_add=True, db_index=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    deleted = models.DateTimeField(_('deleted'), null=True, blank=True, default=None, db_index=True)

    content = models.TextField(_('content'))

    objects = CommentManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._deleted = self.deleted
        self._content = self.content

    def delete(self, using=None, *args, **kwargs):
        if self.children.exists():
            raise SuspiciousOperation('Failed to delete comment with children')

        self.deleted = timezone.now()
        self.save(using=using, update_fields=['deleted'], force_update=True)

    def restore(self, using=None):
        self.deleted = None
        self.save(using=using, update_fields=['deleted'], force_update=True)

    @atomic
    def save(self, *args, **kwargs):
        if self.pk is None:
            action = 'create'
        elif self.deleted is not None and self._deleted is None:
            action = 'delete'
        elif self.deleted is None and self._deleted is not None:
            action = 'restore'
        else:
            action = 'update'

        diff = None
        if action in ('update', 'create'):
            diff = self._get_diff()

        super().save(*args, **kwargs)

        CommentsHistory.objects.create(
            comment=self,
            user_id=storage.get_user_id(),
            action=action,
            diff=diff
        )

    def _get_diff(self) -> list:
        diff = list(differ.compare(self._content.splitlines(True), self.content.splitlines(True)))
        return diff

    def to_dict(self) -> dict:
        data = model_to_dict(self)
        data['created'] = self.created
        data['modified'] = self.modified
        return data

    @property
    def is_root(self) -> bool:
        return self.root_id is None

    @property
    def is_leaf(self) -> bool:
        return not self.children.exists()


class CommentsHistory(models.Model):
    ACTION_CHOICES = (
        ('create', _('create')),
        ('update', _('update')),
        ('delete', _('delete')),
        ('restore', _('restore'))
    )

    comment = models.ForeignKey(Comment, verbose_name=_('comment'), on_delete=models.PROTECT)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    user_id = models.IntegerField(_('user id'))
    action = models.CharField(_('action'), max_length=12, choices=ACTION_CHOICES)
    diff = ArrayField(base_field=models.TextField(), verbose_name=_('content\'s diff'), null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is not None:
            raise SuspiciousOperation('History can not be edited!')

        if self.action in ('update', 'create') and self.diff is None:
            raise ValueError('Field `diff` can not be None for update and create actions')
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        raise SuspiciousOperation('History can not be deleted!')
