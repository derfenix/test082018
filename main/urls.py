from django.urls import path

from main.views import CommentCRUD, CommentsCRUD

app_name = 'main'
urlpatterns = [
    path('comment/<int:pk>/', CommentCRUD.as_view(), name='comment'),
    path('comments/<int:comment_id>/', CommentsCRUD.as_view(), name='comments'),
    path('comments/<int:content_type_id>/<int:object_id>/', CommentsCRUD.as_view(), name='comments'),
    path(
        'comments/<int:content_type_id>/<int:object_id>/first_level/', CommentsCRUD.as_view(),
        name='comments-first_level', kwargs={'first_level': True}
    ),
]
