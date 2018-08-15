import json

from django.views.generic.base import View


class JsonDataMixin(View):
    def json_data(self):
        return json.loads(self.request.body)
