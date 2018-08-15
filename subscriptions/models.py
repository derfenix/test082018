from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _


class Subscription(models.Model):
    user_id = models.IntegerField(_('user id'), db_index=True)

    target = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField(db_index=True)

    class Meta():
        unique_together = ('user_id', 'content_type', 'object_id')
