"""
WSGI config for movie_ticket_assignment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

ENV = os.environ.get("ENV", "dev")
if ENV in ["beta", "prod"]:
    settings = f"movie_ticket_assignment.settings_{ENV}"
else:
    settings = "movie_ticket_assignment.settings"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_ticket_assignment.settings')

application = get_wsgi_application()
