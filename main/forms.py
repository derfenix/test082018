from django import forms

from main.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('parent', 'content_type', 'object_id', 'content')
