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

# importing the geoserver
from geo.Geoserver import Geoserver


conn_str = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( 
    **{
        'user':     DATABASES['default']['USER'],
        'password': DATABASES['default']['PASSWORD'],
        'host':     DATABASES['default']['HOST'],
        'port':     DATABASES['default']['PORT'],
        'dbname':   DATABASES['default']['NAME'],
    }
 )





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


    # it's the same password that we have in settings
    # conn_str = 'postgresql://postgres:password@localhost:5432/geoapp'

    print('shp_file: ', shp_file)
    print('file_name: ', file_name)
    print('file_format: ', file_format)
    print('file_path: ', file_path)

    # with zipfile.ZipFile(shp_file, 'r') as zip_ref:
	#     zip_ref.extractall(file_path)

    if "zip" in file_format:  # this is my idea to check that the uploaded file is a zip one
    # extract zipfile
        with zipfile.ZipFile(shp_file, 'r') as zip_ref:
            zip_ref.extractall(file_path)

        os.remove(shp_file) # remove zip file

    else:
        print("WARNING: shapefile given in input must be in zip format.")

    # Python glob. glob() method returns a list of files or folders that matches the path specified in the pathname argument.
    # https://pynative.com/python-glob/#:~:text=Python%20glob.,UNIX%20shell%2Dstyle%20wildcards).
    shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True)[0] # to get shp
    # devo usare il primo elemento della lista altrimenti il'uscita di glob.glob è una lista

    gdf = gpd.read_file(shp)


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

    gdf.to_sql(file_name, engine, 'public', if_exists='replace', index=False, dtype={'geom': Geometry('Geometry', srid=epsg)})
    # post gdf to the postgresql

    '''
    publish shp to geoserver using geoserver-rest
    '''

    print("getting workspace:", geo.get_workspace('geoApp'))


    geo.create_featurestore(store_name='geoApp', workspace='geoapp', db='geoapp', host='localhost', pg_user='postgres', pg_password='postgres', schema='data')
    # i am adding chema = data perchè shapefile verra pubblicato nello schema di data - controllo su pgadmin
    
    geo.publish_featurestore(store_name='geoApp', workspace='geoapp', pg_table=file_name)

    # geoApp as name of store_name is not really necessary as 

    # workspace si riferisce a geoserver-rest
    #  schema si rieferisce a pgadmin


@receiver(post_delete, sender=Shp)
def delete_data(sender, instance, created, **kwargs):
    pass