import json
from typing import Generator, Collection

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet

__all__ = ['export', 'get_available_formats']

EXPORTERS = {}


def register(name: str):
    """
    Register formatter with specified format name

    Example::

        @register(foo)
        class FooExporter(BaseExporter):
            pass

    :param name: Format name
    """
    def decorator(cls):
        EXPORTERS[name] = cls

        def wrapper(*args, **kwargs):
            return cls(*args, **kwargs)

        return wrapper
    return decorator


def get_available_formats() -> Collection[str]:
    return EXPORTERS.keys()


def export(qs: QuerySet, export_format: str = 'json') -> Generator:
    if export_format not in EXPORTERS:
        raise NotImplementedError('No export class for format {}'.format(export_format))

    exporter_cls = EXPORTERS[export_format]
    exporter = exporter_cls(qs)
    return exporter.export()


class BaseExporter:
    def __init__(self, qs: QuerySet):
        self._qs = qs

    def export(self) -> Generator:
        raise NotImplementedError()

    def rows(self) -> Generator:
        for row in self._qs.iterator():
            yield row.to_dict()


@register('json')
class JsonExporter(BaseExporter):
    def export(self) -> Generator:
        for row in self.rows():
            yield json.dumps(row, cls=DjangoJSONEncoder)
