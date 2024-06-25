from django.db import models
import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import geopandas as gpd

from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement

import os
import zipfile

import glob

# my idea
from geoApp.settings import DATABASES

from geoalchemy2 import Geometry, WKTElement
from geo.Geoserver import Geoserver

# from geo.Geoserver.Postgres import Db
# this one import from venv/lib/site-package/geo/Postgres.py where a Db class is defined
# this is deprecated. this module and class do not exist anymore.

from pg.pg import Pg

# import db credentials, 
# set workspace and store names
# set geoserver credentials
# set connection string (url)
#------------------------------------------------------

# so I don't have to hardcode credentials but just to import them form only one place: settings.py
db_params = {
        'user':     DATABASES['default']['USER'],
        'password': DATABASES['default']['PASSWORD'],
        'host':     DATABASES['default']['HOST'],
        'port':     DATABASES['default']['PORT'],
        'dbname':   DATABASES['default']['NAME'],    
}


# the connection string is created on base of db params defined in settins.py, 

conn_str = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
    **{
        'user':     db_params['user'],
        'password': db_params['password'],
        'host':     db_params['host'],
        'port':     db_params['port'],
        'dbname':   db_params['dbname'],
    }
 )

# the workspace is created once by user in geoserver UI
wks_name='geoapp'

# store_name
ste_name='geoApp'

# schema name
schema_name = 'data'

# layer name
layer_name = wks_name


gsrv_params = {
    'user': 'admin',
    'password': 'geoserver'
}

# initializations
#------------------

# initialize the library
geo = Geoserver(
            'http://127.0.0.1:8080/geoserver', 
            username=gsrv_params['user'], 
            password=gsrv_params['password']
            )


# initialize the Pg class
db = Pg(
    dbname=db_params['dbname'], 
    user=db_params['user'], 
    password=db_params['password'], 
    host=db_params['host'], 
    port=db_params['port']
    )


# class and function definintion
#---------------------------------




# initialize the library
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='geoserver')

# the shapefile model

# Create your models here.
class Shp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    shp_file = models.FileField(upload_to='%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Shp)
def publish_data(sender, instance, created, **kwargs):
    # this will publish the shapefile to the db.
    # the data is first uploaded, then published to the geosverer

    shp_file = instance.shp_file.path
    file_format = os.path.basename(shp_file).split('.')[-1]
    file_name = os.path.basename(shp_file).split('.')[0]
    file_path = os.path.dirname(shp_file)

    inst_name = instance.name
    # it's going to be the same name we have in admin panel


    # it's the same password that we have in settings
    # conn_str = 'postgresql://postgres:password@localhost:5432/geoapp'

    print('shp_file: ', shp_file)
    print('file_name: ', file_name)
    print('file_format: ', file_format)
    print('file_path: ', file_path)

    if "zip" in file_format:  # this is my idea to check that the uploaded file is a zip one
    # extract zipfile
        print("it's a zip")

        with zipfile.ZipFile(shp_file, 'r') as zip_ref:
            zip_ref.extractall(file_path)

        os.remove(shp_file) # remove zip file

    else:
        print("WARNING: shapefile given in input must be in zip format.")

    # Python glob. glob() method returns a list of files or folders that matches the path specified in the pathname argument.
    # https://pynative.com/python-glob/#:~:text=Python%20glob.,UNIX%20shell%2Dstyle%20wildcards).
    shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True) # to get shp
    # se il file è uno zip, devo usare il primo elemento della lista altrimenti il'uscita di glob.glob è una lista
    req_shp = shp[0]

    gdf = gpd.read_file(req_shp)  # make geodataframe


    crs_name = str(gdf.crs.srs)

    print('crs_name: ', crs_name)

    epsg = int(crs_name.lower().replace('epsg:', ''))

    if epsg is None:
        epsg=4326 # wgs84 coordinate system

    geom_type = gdf.geom_type[1]

    engine = create_engine(conn_str)  # create the SQLAlchemy engine to use

    gdf['geom'] = gdf['geometry'].apply(lambda x: WKTElement(x.wkt, srid=epsg))

    gdf.drop('geometry', 1, inplace=True)  # drop the geometry column since we already bckup this column with geom
    # In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only.

    # post gdf to the postgresql
    # gdf.to_sql(file_name, engine, 'public', if_exists='replace', index=False, dtype={'geom': Geometry('Geometry', srid=epsg)})
    # for the name of the tabel, I can now just put the name of the instance uploaded
    gdf.to_sql(inst_name, 
               engine, 
               'public', 
               if_exists='replace', 
               index=False, 
               dtype={
                   'geom': Geometry('Geometry', srid=epsg)
                   }
                )

    '''
    publish shp to geoserver using geoserver-rest
    '''

    print("getting workspace:", geo.get_workspace('geoApp'))

    geo.create_featurestore(workspace=wks_name, 
                            store_name=ste_name, 
                            db=db_params['dbname'], 
                            host=db_params['host'], 
                            pg_user=db_params['postgres'], 
                            pg_password=db_params['password'])
    # shapefile will be published in "data" schema

    # geo.publish_featurestore(workspace=wks_name, store_name=ste_name, pg_table=file_name)
    # for the name of the tabel, I can now just put the name of the instance uploaded
    geo.publish_featurestore(workspace=wks_name, 
                             store_name=ste_name, 
                             pg_table=inst_name)

    

    geo.create_featurestore(store_name='geoApp', workspace='geoapp', db='geoapp', host='localhost', pg_user='postgres', pg_password='postgres', schema='data')
    # i am adding chema = data perchè shapefile verra pubblicato nello schema di data - controllo su pgadmin
    
    geo.publish_featurestore(store_name='geoApp', workspace='geoapp', pg_table=file_name)

    # geoApp as name of store_name is not really necessary as 

    # workspace si riferisce a geoserver-rest
    #  schema si rieferisce a pgadmin


@receiver(post_delete, sender=Shp)
def delete_data(sender, instance, **kwargs):
    # the content of this class is somehow copied from venv/lib/site-package/geo/Postgres.py 
    inst_name = instance.name

    db.delete_table(
            table_name=inst_name,
            schema=schema_name,
            dbname=db_params['dbname']) 
    # again, here i take directly the name of the uploaded instance
    
    geo.delete_layer(inst_name, layer_name)

    pass