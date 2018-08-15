import json

from django.test import TestCase

from main.export import export
from main.models import Comment
from test082018.local_storage import storage


class ExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        storage.set_user_id(100)
        for idx in range(10):
            Comment.objects.create(
                user_id=(100 + idx),
                content_type_id=1,
                object_id=1,
                content='Comment {}'.format(idx)
            )

    def test_bad_export_format(self):
        qs = Comment.objects.all()
        with self.assertRaisesMessage(NotImplementedError, 'No export class for format foobar'):
            export(qs, export_format='foobar')

    def test_json_exporter(self):
        qs = Comment.objects.all()
        gen = export(qs, export_format='json')
        data = [json.loads(x) for x in gen]
        self.assertEqual(len(data), 10)
        self.assertEqual(
            set(data[0].keys()),
            {
                'id', 'root', 'parent', 'level', 'user_id', 'content_type', 'object_id',
                'created', 'modified', 'deleted', 'content'
            }
        )
