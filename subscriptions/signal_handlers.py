from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import CommentsHistory
from subscriptions.tools import send_push
from subscriptions.models import Subscription


@receiver(post_save, sender=CommentsHistory, dispatch_uid='notify_about_comments_changes')
def notify_about_comments_changes(instance: CommentsHistory, created, **kwargs):
    if not created:
        return

    subscriptions = Subscription.objects.filter(content_type_id=instance.comment.content_type_id,
                                                object_id=instance.comment.object_id)
    if not subscriptions.exists():
        return

    user_ids = set(subscriptions.values_list('user_id', flat=True)) - {instance.user_id}
    if len(user_ids) == 0:
        return

    data = {
        'diff': instance.diff,
        'action': instance.action,
        'action_verbose': instance.get_action_display(),
        'timestamp': instance.timestamp,
        'comment': instance.comment.content,
        'author': instance.user_id
    }

    send_push(user_ids, data)
