from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic.base import View

from subscriptions.models import Subscription
from test082018.local_storage import storage


class SubscriptionView(View):
    model = Subscription

    def post(self, request, content_type_id, object_id):
        try:
            target_model = ContentType.objects.get_for_id(content_type_id)
        except ContentType.DoesNotExist:
            raise Http404()

        if not target_model.objects.filter(pk=object_id).exists():
            raise Http404()

        subscription, created = self.model.objects.get_or_create(
            content_type_id=content_type_id,
            object_id=object_id,
            user_id=storage.get_user_id()
        )

        return JsonResponse({'status': 'created' if created else 'exists'}, status=201 if created else 200)

    def delete(self, request, content_type_id, object_id):
        qs = self.model.objects.filter(
            content_type_id=content_type_id,
            object_id=object_id,
            user_id=storage.get_user_id()
        )
        if not qs.exists():
            raise Http404()

        qs.delete()
        return HttpResponse(status=200)
