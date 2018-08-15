from typing import Optional

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from common.json_views import JsonDataMixin
from main.forms import CommentForm
from main.models import Comment
from test082018.local_storage import storage


class CommentCRUD(JsonDataMixin, View):
    model = Comment
    form = CommentForm

    def get(self, request, pk: int) -> HttpResponse:
        comment = get_object_or_404(self.model, pk=pk)
        return JsonResponse(comment.to_dict())

    def put(self, request, pk: int) -> HttpResponse:
        comment = get_object_or_404(self.model, pk=pk)
        comment.content = self.json_data().get('content')
        comment.save()
        return HttpResponse(status=200)

    def delete(self, request, pk: int) -> HttpResponse:
        comment = get_object_or_404(self.model, pk=pk)
        comment.delete()
        return HttpResponse(status=200)

    def post(self, request, pk: int) -> HttpResponse:
        comment = get_object_or_404(self.model, pk=pk)
        new_comment = self.model.objects.create(
            user_id=storage.get_user_id(),
            content_type_id=comment.content_type_id,
            object_id=comment.object_id,
            level=(comment.level + 1),
            parent_id=comment.id,
            root_id=comment.root_id or comment.pk,
            content=self.json_data().get('content')
        )
        return JsonResponse({'pk': new_comment.pk}, status=201)


class CommentsCRUD(JsonDataMixin, View):
    model = Comment
    form = CommentForm
    page_size = 50

    def get(self, request: HttpRequest, comment_id: Optional[int] = None, first_level: Optional[bool] = False,
            content_type_id: Optional[int] = None, object_id: Optional[int] = None) -> HttpResponse:
        if not comment_id and not (content_type_id and object_id):
            raise Http404()

        if comment_id is not None:
            comments = self.model.objects.filter(root_id=comment_id)
        else:
            comments = self.model.objects.filter(content_type_id=content_type_id, object_id=object_id)
            if first_level:
                comments = comments.filter(parent=None)
                paginator = Paginator(comments, request.GET.get('page_size', self.page_size))
                comments = paginator.get_page(request.GET.get('page', 1))

        comments = comments.values()
        return JsonResponse([comment for comment in comments], safe=False)

    def post(self, request, content_type_id: Optional[int] = None, object_id: Optional[int] = None) -> HttpResponse:
        new_comment = self.model.objects.create(
            user_id=storage.get_user_id(),
            content_type_id=content_type_id,
            object_id=object_id,
            level=0,
            content=self.json_data().get('content')
        )
        return JsonResponse({'pk': new_comment.pk}, status=201)
