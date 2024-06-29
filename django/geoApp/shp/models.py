from django.db import models
import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import geopandas as gpd

import os
import shutil
import zipfile

import glob

# from sqlalchemy import Geometry, WKTElement
from sqlalchemy import *
from geo.Geoserver import Geoserver

# from geo.Geoserver.Postgres import Db
# this one import from venv/lib/site-package/geo/Postgres.py where a Db class is defined
# this is deprecated. this module and class do not exist anymore.

from pg.pg import Pg  # postgres-helper library made by the course author

from shp.configs import DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP
from shp.configs import UPLOADED_SHP_FILES_MUST_BE_ZIPPED

from geoApp.geo_system_configs import GEOSERVER_CREDENTIALS
from geoApp.geo_system_configs import geoapp_db_params

from geoApp.geo_system_configs import \
                        wksp_name,  \
                        ste_name,   \
                        schm_name,  \
                        layr_name,  \
                        sty_name    \
                        
from shp.configs import generate_uploaded_shp_file_relpath
from shp.configs import UPLOADED_SHP_FILES_FOLDER_DIR

from geoApp.settings import BASE_DIR

from django.core.exceptions import ValidationError

from shp.instantiate_connections import \
                                        geo,        \
                                        db,         \
                                        conn_str    \
                                    
from shp.process_shapefile import publish_shp_geo_data

from geoApp.geo_system_check import check_geoserver_status
from geoApp.exceptions import GeoserverNotAvailableError

# import db credentials, 
# set workspace and store names
# set geoserver credentials
# set connection string (url)
#------------------------------------------------------


# class and function definintion
#---------------------------------




# the shapefile model


# Create your models here.
class Shp(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    shp_file = models.FileField(upload_to="shp/%Y%m%d_%H%M%S") 
    # shp_file = models.FileField(upload_to=generate_uploaded_shp_file_relpath(UPLOADED_SHP_FILES_FOLDER_DIR) ) 
    
     # this is a file, but in postgres is represented as path

    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    shp_file_folder_path = models.CharField(default='undefined', max_length=1000, blank=True)  
    # maybe here is not important the default value to be correct, because it will be overwritten by the save method
    # this is to be not visible nor editable by admins

    def __str__(self):
        return "{} - {}".format(self.id, self.name)
    
    def clean(self):
        super().clean()
        if UPLOADED_SHP_FILES_MUST_BE_ZIPPED:
            print("File validation: UPLOADED_SHP_FILES_MUST_BE_ZIPPED")
            if not self.shp_file.name.endswith('.zip'):
                raise ValidationError('The file must have .zip extension.')
            else:
                print("> validation passed!")
                pass

    def save(self, *args, **kwargs):
        print("custom Shp save method - ACTIVATES")
        super().save(*args, **kwargs)

        print("File saved at path {}".format(self.shp_file.path))

        # update value of shp_file_folder_path
        # print("Name:", self.shp_file.name)
        # print("Path:", self.shp_file.path)
        # print("URL:", self.shp_file.url)
        # print("Size:", self.shp_file.size)
        # print("File:", self.shp_file.file)

        self.shp_file_folder_path = os.path.dirname( self.shp_file.path )

        # -------------- receiver logic -------------------

        
        check_geoserver_status()
        

        publish_shp_geo_data(self)


        super().save(*args, **kwargs)

        # here the receivers can be triggered

#--------------------------------------------------

    # def delete(self, *args, **kwargs):
    # this method does not work - do not use it. use receivers
    #     print("remove file at path {}".format(self.shp_file.path))
    #     try:
    #         os.remove(self.shp_file.path)
    #     except Exception as e:
    #         print("could not delete file {}".format(self.shp_file.path))

    #     # Chiama il metodo delete del genitore
    #     super().delete(*args, **kwargs)

#----------------------------------


# method 2 to delete the file associated with the model
@receiver(post_delete, sender=Shp)
def delete_file_on_model_shp_delete(sender, instance, **kwargs):
    # if instance.shp_file:
    #     if os.path.isfile(instance.shp_file.path):
    #         os.remove(instance.shp_file.path)
    try:
        # os.remove(instance.shp_file.path)
        shutil.rmtree(instance.shp_file_folder_path)
        print("Deleted folder {}".format(instance.shp_file_folder_path))
    except Exception as e:
        print("Could not delete folder {}\n{}".format(instance.shp_file_folder_path, e))


@receiver(post_delete, sender=Shp)
def delete_geo_data_on_model_shp_delete(sender, instance, **kwargs):
    print("@receiver 'delete_geo_data_on_model_shp_delete' - ACTIVATES")
    # # the content of this class is somehow copied from venv/lib/site-package/geo/Postgres.py 
    
    instance_name = instance.name

    # delete the content that was sent to_postgis
    db.delete_table(
            instance_name,
            schema=schm_name
            ) 
    # again, here I take directly the name of the uploaded instance
    
    # delete the layer
    geo.delete_layer(instance_name, layr_name)

    # remove object form geoserver
    geo.delete_layer(instance.name, layr_name)



    