from django.contrib import admin

# make my model accessible from the admin interface
from .models import Shp

# Register your models here.
admin.site.register(Shp)