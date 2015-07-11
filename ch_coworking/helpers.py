from django.conf import settings
from elasticsearch import Elasticsearch

class ChHelpers(object):
    @staticmethod
    def get_es():
        return Elasticsearch(
            hosts=[settings.ELASTICSEARCH['url']]
        )
