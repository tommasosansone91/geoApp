from django.db import models
import datetime

from django.db.models.signals import post_delete
from django.dispatch import receiver

import os
import shutil

from sqlalchemy import *

from geoApp.geo_system_configs import \
                        wksp_name,  \
                        ste_name,   \
                        schm_name

                        

from django.core.exceptions import ValidationError

from geoApp.instantiate_connections import \
                                        geo,        \
                                        db,         \
                                        conn_str    \
                                    
from tiff.process_tiff import publish_tiff_geo_data

from geoApp.geo_system_check import check_geoserver_status
from geoApp.exceptions import GeoserverNotAvailableError


# ensure geoserver is active, otherwise, do not allow the app to start
check_geoserver_status()
# here the error raised by check_geoserver_status() is not managed.
# so if it occurs, it crashes the app.

# Create your models here.
class Tiff(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    tiff_file = models.FileField(upload_to="tiff/%Y%m%d_%H%M%S") 
    # tiff_file = models.FileField(upload_to=generate_uploaded_tiff_file_relpath(UPLOADED_TIFF_FILES_FOLDER_DIR) ) 
    
     # this is a file, but in postgres is represented as path

    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    tiff_file_folder_path = models.CharField(default='undefined', max_length=1000, blank=True)  
    # maybe here is not important the default value to be correct, because it will be overwritten by the save method
    # this is to be not visible nor editable by admins


    def __str__(self):
        return "{} - {}".format(self.id, self.name)

    def clean(self):
        super().clean()

        print("File validation: uploaded tiff files must have .tif or .tiff extension")
        if not self.tiff_file.name.endswith('.tif') and not self.tiff_file.name.endswith('.tiff'):
            raise ValidationError("The file must have .tif or .tiff extension.")
        else:
            print("> validation passed!")
            pass

    def save(self, *args, **kwargs):
        print("custom Tiff save method - ACTIVATES - Instance: {}".format(self))

        try:
            check_geoserver_status()
        except GeoserverNotAvailableError as e:
            print(e)
            # here the error raised by check_geoserver_status() is intercepted and managed,
            # then allowing the app to launch a return to 
            # prevent data save
            return
        
        super().save(*args, **kwargs)

        print("Tiff file saved at path {}".format(self.tiff_file.path))

        # print("Name:", self.tiff_file.name)
        # print("Path:", self.tiff_file.path)
        # print("URL:", self.tiff_file.url)
        # print("Size:", self.tiff_file.size)
        # print("File:", self.tiff_file.file)

        # update value of tiff_file_folder_path
        self.tiff_file_folder_path = os.path.dirname( self.tiff_file.path )

        # -------------- receiver logic -------------------       
        
        publish_tiff_geo_data(self)

        super().save(*args, **kwargs)

#--------------------------------------------------

    # def delete(self, *args, **kwargs):
    # this method does not work - do not use it. use receivers
    #     print("remove file at path {}".format(self.tiff_file.path))
    #     try:
    #         os.remove(self.tiff_file.path)
    #     except Exception as e:
    #         print("could not delete file {}".format(self.tiff_file.path))

    #     # Chiama il metodo delete del genitore
    #     super().delete(*args, **kwargs)

#----------------------------------


# method 2 to delete the file associated with the model
@receiver(post_delete, sender=Tiff)
def delete_file_on_model_tiff_delete(sender, instance, **kwargs):
    print("@receiver 'delete_file_on_model_tiff_delete' - Instance: {}".format(instance))
    # delete the folder

    try:
        shutil.rmtree(instance.tiff_file_folder_path)
        print("Deleted folder {}".format(instance.tiff_file_folder_path))
    except Exception as e:
        print("Could not delete folder {}\n{}".format(instance.tiff_file_folder_path, e))


@receiver(post_delete, sender=Tiff)
def delete_geo_data_on_model_tiff_delete(sender, instance, **kwargs):
    print("@receiver 'delete_geo_data_on_model_tiff_delete' - Instance: {}".format(instance))
    
    instance_name = instance.name

    # nothing was sent to_postgis

    # delete the layer
    geo.delete_layer(instance_name, wksp_name)

    print("Deleted tiff layer {}".format(instance_name))
