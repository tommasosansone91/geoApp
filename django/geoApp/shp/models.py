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

from geoApp.settings import GEOSERVER_CREDENTIALS
from geoApp.settings import geoapp_db_params

from shp.configs import \
                        wksp_name,  \
                        ste_name,   \
                        schm_name,  \
                        layr_name,  \
                        sty_name    \
                        
from shp.configs import generate_uploaded_shp_file_relpath
from shp.configs import UPLOADED_SHP_FILES_FOLDER_DIR

from geoApp.settings import BASE_DIR


from django.core.exceptions import ValidationError

# import db credentials, 
# set workspace and store names
# set geoserver credentials
# set connection string (url)
#------------------------------------------------------


# initializations
#------------------

# initialize the Pg class
db = Pg(
    dbname=geoapp_db_params['dbname'], 
    user=geoapp_db_params['user'], 
    password=geoapp_db_params['password'], 
    host=geoapp_db_params['host'], 
    port=geoapp_db_params['port']
    )

# initialize the library
geo = Geoserver(
            'http://127.0.0.1:8080/geoserver', 
            username=GEOSERVER_CREDENTIALS['user'], 
            password=GEOSERVER_CREDENTIALS['password']
            )
#aligned

# the connection string is created on base of db params defined in settins.py, 
conn_str = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( **geoapp_db_params )

print(
"""
credentials:
-------------

geoapp_db_params
{}

GEOSERVER_CREDENTIALS: 
{}

conn_str: 
{}

      
""".format(geoapp_db_params, GEOSERVER_CREDENTIALS, conn_str)
)



# class and function definintion
#---------------------------------

class NotAZipFileError(Exception):
    pass

class NotAShapefileError(Exception):
    pass

class NoShapeFileFoundError(Exception):
    pass

class TooManyShapeFileFoundError(Exception):
    pass



# the shapefile model


# Create your models here.
class Shp(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    shp_file = models.FileField(upload_to=generate_uploaded_shp_file_relpath(UPLOADED_SHP_FILES_FOLDER_DIR)) 
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
                print("validation passed")
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

        super().save(*args, **kwargs)

        # here the receivers can be triggered


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


@receiver(post_save, sender=Shp)
def publish_geo_data_on_model_shp_save(sender, instance, created, **kwargs):
    # this will publish the shapefile to the db.
    # the data is first uploaded, then published to the geosverer

    print("@receiver 'publish_geo_data_on_model_shp_save' - ACTIVATES")

    shp_file_abspath = instance.shp_file.path
    file_name = os.path.basename(shp_file_abspath)
    file_format = os.path.basename(shp_file_abspath).split('.')[-1]
    file_name_noext = os.path.basename(shp_file_abspath).split('.')[0]  # without the format
    shp_file_folder_abspath = os.path.dirname(shp_file_abspath)

    instance_name = instance.name
#     # it's going to be the same name we have in admin panel

    print('shp_file_abspath: ', shp_file_abspath)
    print('file_name: ', file_name)
    print('file_name_noext: ', file_name_noext)
    print('file_format: ', file_format)
    print('shp_file_folder_abspath: ', shp_file_folder_abspath)

    if DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP:
        if "zip" in file_format:  # this is my idea to check that the uploaded file is a zip one
        # extract zipfile
            print(
                "{} is a zip file!\nExtracting content in folder {}".format(
                file_name, shp_file_folder_abspath)
                )

            zip_file_abspath = shp_file_abspath

            with zipfile.ZipFile(zip_file_abspath, 'r') as zip_ref:
                zip_ref.extractall(shp_file_folder_abspath)

            os.remove(zip_file_abspath)  # remove zip file

        else:
            if UPLOADED_SHP_FILES_MUST_BE_ZIPPED:
                raise NotAZipFileError("ERROR: The shapefile given in input must be in zip format. It is {}".format(file_format))



    # Python glob. glob() method returns a list of files or folders that matches the path specified in the pathname argument.
    # https://pynative.com/python-glob/#:~:text=Python%20glob.,UNIX%20shell%2Dstyle%20wildcards).
    
    shp_files_list = glob.glob(
        r'{}/**/*.shp'.format(shp_file_folder_abspath), 
        recursive=True
        ) # to get shp, among the n files inside the zip
    # se il file è uno zip, devo usare il primo elemento della lista altrimenti il'uscita di glob.glob è una lista

    #  cerca tutti i file con estensione .shp all'interno della directory specificata da shp_file_folder_abspath 
    # e in tutte le sue sottodirectory 
    # e restituisce una lista di questi percorsi di file.

    print(shp_files_list)

    if len(shp_files_list) == 0:
        raise NoShapeFileFoundError("No shapefile found.")

    if len(shp_files_list) > 1:
        raise TooManyShapeFileFoundError("Too many shapefile found.")
    
    try:
        req_shp = shp_files_list[0]

        gdf = gpd.read_file(req_shp)  # make geodataframe

        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema=schm_name,
            name=instance_name,
            if_exists="replace")
            # how to manage the fact that an instance could overwrite another on geoserver 
            # but not on django model ?
            # see geopandas options

        print("instance {} was sent to_postgis!".format(instance_name))

        for s in shp_files_list:
            os.remove(s)

    except Exception as e:
        for s in shp_files_list:
            os.remove(s)

        instance.delete()
        print("There was a problem during shp upload: ", e)
        print("Shp instance {} was deleted".format(shp_file_abspath))


    '''
    publish shp to geoserver using geoserver-rest
    '''

    # check that the elements exists
    if not geo.get_workspace(wksp_name):
        print("create workspace '{}'".format(wksp_name))
        geo.create_workspace(wksp_name)


    # print("getting workspace:", geo.get_workspace(wksp_name))

    geo.create_featurestore(workspace=wksp_name, 
                            store_name=ste_name, 
                            schema=schm_name,
                            db=geoapp_db_params['dbname'], 
                            host=geoapp_db_params['host'], 
                            pg_user=geoapp_db_params['user'], 
                            pg_password=geoapp_db_params['password']
                            )
    # shapefile will be published in "data" schema
    # print("created featurestore: {}".format(ste_name))
    # print(wksp_name, ste_name, schm_name, geoapp_db_params['dbname'],geoapp_db_params['host'],geoapp_db_params['user'], geoapp_db_params['password'])

    # geo.publish_featurestore(workspace=wksp_name, store_name=ste_name, pg_table=file_name_noext)
    # for the name of the tabel, I can now just put the name of the instance uploaded
    geo.publish_featurestore(workspace=wksp_name, 
                             store_name=ste_name, 
                             pg_table=instance_name)
    print("published featurestore: {}\npg_table: {}".format(ste_name, instance_name))


    # edit style
    geo.create_outline_featurestyle(sty_name, 
                                    workspace=wksp_name)
    # the first argument is the output style name

    geo.publish_style(
        layer_name=layr_name, 
        style_name=sty_name, 
        workspace=wksp_name)
    print("published style {} for layer {}".format(sty_name, layr_name))


    # workspace si riferisce a geoserver-rest
    #  schema si rieferisce a pgadmin


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



    