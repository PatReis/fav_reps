"""
WSGI config for favourite_recipes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# ROOT_DIR = "/home/patrick/django-apps/fav_reps/"
# sys.path.append(ROOT_DIR)
# os.chdir(ROOT_DIR)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'favourite_recipes.settings')
os.environ["DJANGO_SETTINGS_MODULE"] = "favourite_recipes.settings"

application = get_wsgi_application()
