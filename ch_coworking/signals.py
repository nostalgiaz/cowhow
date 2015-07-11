from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ch_coworking.helpers import ChHelpers
from ch_coworking.models import Coworking


@receiver(post_save, sender=Coworking,
          dispatch_uid='ch_coworking.signals.coworking_post_save')
def coworking_post_save(sender, instance, created, **kwargs):
    client = ChHelpers.get_es()
    try:
        client.delete(
            index=settings.ELASTICSEARCH['index'],
            doc_type=settings.ELASTICSEARCH['doc_type'],
            id=instance.pk
        )
    except:
        pass

    try:
      client.index(
          index=settings.ELASTICSEARCH['index'],
          doc_type=settings.ELASTICSEARCH['doc_type'],
          id=instance.pk,
          body={
              'name': instance.name,
              'location': {
                  'lat': instance.lat,
                  'lon': instance.lng
              }
          }
      )
    except:
        pass
