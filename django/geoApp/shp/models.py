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

class NotAZIPFileError(Exception):
    pass

class NotAShapefileError(Exception):
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
            if not self.shp_file.name.endswith('.zip'):
                raise ValidationError('The file must have .zip extension.')

    def save(self, *args, **kwargs):

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


    # def delete(self, *args, **kwargs):
    # this method does not work - do not use it. use receivers
    #     print("remove file at path {}".format(self.shp_file.path))
    #     try:
    #         os.remove(self.shp_file.path)
    #     except Exception as e:
    #         print("could not delete file {}".format(self.shp_file.path))

    #     # Chiama il metodo delete del genitore
    #     super().delete(*args, **kwargs)

# #----------------------------------


# @receiver(post_save, sender=Shp)
# def publish_data(sender, instance, created, **kwargs):
#     # this will publish the shapefile to the db.
#     # the data is first uploaded, then published to the geosverer

#     print("@receiver 'publish_data' - activates")

#     ffile = instance.shp_file.path
#     file_format = os.path.basename(ffile).split('.')[-1]
#     file_name = os.path.basename(ffile).split('.')[0]  # without the format
#     file_path = os.path.dirname(ffile)

#     instance_name = instance.name
# #     # it's going to be the same name we have in admin panel

#     print('ffile: ', ffile)
#     print('file_name: ', file_name)
#     print('file_format: ', file_format)
#     print('file_path: ', file_path)

#     if DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP:
#         if "zip" in file_format:  # this is my idea to check that the uploaded file is a zip one
#         # extract zipfile
#             print("ok, it is a zip.")

#             with zipfile.ZipFile(zip_file_abspath, 'r') as zip_ref:
#                 zip_ref.extractall(file_path)

#             os.remove(zip_file_abspath) # remove zip file

#         else:
#             raise NotAZIPFileError("ERROR: The shapefile given in input must be in zip format. It is {}".format(file_format))
#             # qui serve che si inneschi un delete senza raise error.

#     # Python glob. glob() method returns a list of files or folders that matches the path specified in the pathname argument.
#     # https://pynative.com/python-glob/#:~:text=Python%20glob.,UNIX%20shell%2Dstyle%20wildcards).
#     shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True) # to get shp, among the n files inside the zip
#     # se il file è uno zip, devo usare il primo elemento della lista altrimenti il'uscita di glob.glob è una lista

#     #  cerca tutti i file con estensione .shp all'interno della directory specificata da file_path 
#     # e in tutte le sue sottodirectory 
#     # e restituisce una lista di questi percorsi di file.

#     print(shp)

#     try:
#         req_shp = shp[0]

#         gdf = gpd.read_file(req_shp)  # make geodataframe

#         engine = create_engine(conn_str)
#         gdf.to_postgis(
#             con=engine,
#             schema=schm_name,
#             name=instance_name,
#             if_exists="replace")

#         for s in shp:
#             os.remove(s)

#     except Exception as e:
#         for s in shp:
#             os.remove(s)

#         instance.delete()
#         print("There is problem during shp upload: ", e)
    
#     # req_shp = shp[0]

#     # gdf = gpd.read_file(req_shp)  # make geodataframe


#     # crs_name = str(gdf.crs.srs)

#     # print('crs_name: ', crs_name)

#     # epsg = int(crs_name.lower().replace('epsg:', ''))

#     # if epsg is None:
#     #     epsg=4326 # wgs84 coordinate system

#     # geom_type = gdf.geom_type[1]

#     # engine = create_engine(conn_str)  # create the SQLAlchemy engine to use

#     # gdf['geom'] = gdf['geometry'].apply(lambda x: WKTElement(x.wkt, srid=epsg))

#     # gdf.drop('geometry', 1, inplace=True)  # drop the geometry column since we already bckup this column with geom
#     # # In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only.

#     # # post gdf to the postgresql
#     # # gdf.to_sql(file_name, engine, 'public', if_exists='replace', index=False, dtype={'geom': Geometry('Geometry', srid=epsg)})
#     # # for the name of the tabel, I can now just put the name of the instance uploaded
#     # gdf.to_sql(instance_name, 
#     #            engine, 
#     #            'public', 
#     #            if_exists='replace', 
#     #            index=False, 
#     #            dtype={
#     #                'geom': Geometry('Geometry', srid=epsg)
#     #                }
#     #             )

#     '''
#     publish shp to geoserver using geoserver-rest
#     '''

#     # check that the elements exists
#     if not geo.get_workspace(wksp_name):
#         print("create workspace '{}'".fomat(wksp_name))
#         geo.create_workspace(wksp_name)


#     # print("getting workspace:", geo.get_workspace(wksp_name))

#     geo.create_featurestore(workspace=wksp_name, 
#                             store_name=ste_name, 
#                             schema=schm_name,
#                             db=geoapp_db_params['dbname'], 
#                             host=geoapp_db_params['host'], 
#                             pg_user=geoapp_db_params['user'], 
#                             pg_password=geoapp_db_params['password']
#                             )
#     # shapefile will be published in "data" schema
#     print("create featurestore")
#     # print(wksp_name, ste_name, schm_name, geoapp_db_params['dbname'],geoapp_db_params['host'],geoapp_db_params['user'], geoapp_db_params['password'])

#     # geo.publish_featurestore(workspace=wksp_name, store_name=ste_name, pg_table=file_name)
#     # for the name of the tabel, I can now just put the name of the instance uploaded
#     geo.publish_featurestore(workspace=wksp_name, 
#                              store_name=ste_name, 
#                              pg_table=instance_name)
#     print("publish featurestore")


#     # edit style
#     geo.create_outline_featurestyle(sty_name, 
#                                     workspace=wksp_name)
#     # the first argument is the output style name

#     geo.publish_style(
#         layer_name=layr_name, 
#         style_name=sty_name, 
#         workspace=wksp_name)
#     print("publish style")


#     # workspace si riferisce a geoserver-rest
#     #  schema si rieferisce a pgadmin

# method 2 to delete the file associated with the model
@receiver(post_delete, sender=Shp)
def delete_file_on_model_delete(sender, instance, **kwargs):
    # if instance.shp_file:
    #     if os.path.isfile(instance.shp_file.path):
    #         os.remove(instance.shp_file.path)
    try:
        # os.remove(instance.shp_file.path)
        shutil.rmtree(instance.shp_file_folder_path)
        print("Deleted folder {}".format(instance.shp_file_folder_path))
    except Exception as e:
        print("Could not delete folder {}\n{}".format(instance.shp_file_folder_path, e))


# @receiver(post_delete, sender=Shp)
# def delete_data(sender, instance, **kwargs):
#     print("@receiver 'delete_data' activates")
#     # # the content of this class is somehow copied from venv/lib/site-package/geo/Postgres.py 
#     # instance_name = instance.name

#     # db.delete_table(
#     #         instance_name,
#     #         schema=schm_name
#     #         ) 
#     # # again, here i take directly the name of the uploaded instance
    
#     # geo.delete_layer(instance_name, layr_name)

#     # pass

#     # remove object from db
#     db.delete_table(instance.name, schema=schm_name)

#     # remove object form geoserver
#     geo.delete_layer(instance.name, layr_name)

#     # remove files form local dir

#     zip_file_abspath = instance.shp_file.path
#     print("zip_file_abspath", zip_file_abspath)
#     # zip_file_format = os.path.basename(zip_file_abspath).split('.')[-1]
#     file_name = os.path.basename(zip_file_abspath).split('.')[0]
#     print("file_name", file_name)


#     unpacked_files_dir = os.path.dirname(zip_file_abspath)

#     print("delete directory '{}' and all files inside it".format(unpacked_files_dir))
#     # shutil.rmtree(unpacked_files_dir)

#     file_path = os.path.dirname(zip_file_abspath)



    