from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from ch_coworking.helpers import ChHelpers
from ch_coworking.models import Coworking, Table


def insert_coworking(instance):
    client = ChHelpers.get_es()

    try:
        client.delete(
            index=settings.ELASTICSEARCH['index'],
            doc_type=settings.ELASTICSEARCH['doc_type'],
            id=instance.pk
        )
    except:
        pass

    client.index(
        index=settings.ELASTICSEARCH['index'],
        doc_type=settings.ELASTICSEARCH['doc_type'],
        id=instance.pk,
        body={
            'name': instance.name,
            'location': {
                'lat': instance.lat,
                'lon': instance.lng
            },
            'amenities': [a.name for a in instance.amenities.all()],
            'photos': [a.photo.url for a in instance.photos.all()],
            'tables': [{
                'name': t.name,
                'price': t.price,
                'pk': t.pk,
            } for t in instance.tables.all()]
        }
    )


@receiver(m2m_changed, sender=Coworking.amenities.through,
          dispatch_uid='ch_coworking.signals.coworking_m2m_save')
@receiver(post_save, sender=Coworking,
          dispatch_uid='ch_coworking.signals.coworking_post_save')
def coworking_post_save(sender, instance, **kwargs):
    insert_coworking(instance)


@receiver(post_save, sender=Table,
          dispatch_uid='ch_coworking.signals.table_post_save')
def table_post_save(sender, instance, **kwargs):
    insert_coworking(instance.coworking)
