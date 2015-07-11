from __future__ import unicode_literals, print_function

from django.conf import settings
from django.core.management.base import NoArgsCommand

from ch_coworking.helpers import ChHelpers


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        es = ChHelpers.get_es()
        indices = es.indices

        index = settings.ELASTICSEARCH['index']
        doc_type = settings.ELASTICSEARCH['doc_type']

        if indices.exists(index):
            indices.delete(index)

        indices.create(index, {
            'mappings': {
                doc_type: {
                    'properties': {
                        'location': {
                            'type': 'geo_point',
                            'store': True
                        }
                    }
                }
            }
        })
