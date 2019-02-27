"""
WSGI config for DrScratch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drScratch.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = "drScratch.settings"

import django
django.setup()

#activate_this = "/home/dsadmin/.virtualenvs/virtualenv_drscratchv3/bin/activate_this.py"
#execfile(activate_this, dict(__file__=activate_this))

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
