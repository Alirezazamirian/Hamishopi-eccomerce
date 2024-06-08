from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_save


class AccountModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_module'

