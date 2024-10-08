# this file must be given in input to gunicorn, 
# and it is better that remains in root directory of the application.

import os
from django.core.wsgi import get_wsgi_application

# environment settings for Django app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoApp.settings')

# Initialize app Django
application = get_wsgi_application()
