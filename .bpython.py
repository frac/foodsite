from django.core.management import setup_environ
import settings
setup_environ(settings)
#from minha_app.models import * # opcional
from settings import INSTALLED_APPS
