import braintree

from django.apps import AppConfig
from django.conf import settings


class ChCoworkingConfig(AppConfig):
    name = 'ch_coworking'
    verbose_name = "Coworking"

    def ready(self):
        from . import signals # noqa

        merchant_id = settings.BRAINTREE_MERCHANT_ID
        public_key = settings.BRAINTREE_PUBLIC_KEY
        private_key = settings.BRAINTREE_PRIVATE_KEY

        if settings.BRAINTREE_SANDBOX:
            env = braintree.Environment.Sandbox
        else:
            env = braintree.Environment.Production

        if all((merchant_id, public_key, private_key)):
            try:
                braintree.Configuration.configure(
                    env,
                    merchant_id,
                    public_key,
                    private_key
                )
            except Exception:
                pass
