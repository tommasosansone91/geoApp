from django.db import models
import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import geopandas as gpd

import os
import zipfile

import glob

# from sqlalchemy import Geometry, WKTElement
from sqlalchemy import *
from geo.Geoserver import Geoserver

# from geo.Geoserver.Postgres import Db
# this one import from venv/lib/site-package/geo/Postgres.py where a Db class is defined
# this is deprecated. this module and class do not exist anymore.

from pg.pg import Pg  # postgres-helper library made by the course author

from geoApp.settings import DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP
from geoApp.settings import GEOSERVER_CREDENTIALS

from shp.configs import uploaded_shp_files_relpath
from shp.configs import db_params
from shp.configs import \
                        wksp_name,  \
                        ste_name,   \
                        schm_name,  \
                        layr_name,  \
                        sty_name    \

# import db credentials, 
# set workspace and store names
# set geoserver credentials
# set connection string (url)
#------------------------------------------------------


# initializations
#------------------

# initialize the Pg class
db = Pg(
    dbname=db_params['dbname'], 
    user=db_params['user'], 
    password=db_params['password'], 
    host=db_params['host'], 
    port=db_params['port']
    )

# initialize the library
geo = Geoserver(
            'http://127.0.0.1:8080/geoserver', 
            username=GEOSERVER_CREDENTIALS['user'], 
            password=GEOSERVER_CREDENTIALS['password']
            )
#aligned

# the connection string is created on base of db params defined in settins.py, 
conn_str = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( **db_params )

print("conn_str:\n{}".format(conn_str))




# class and function definintion
#---------------------------------

class NotAZIPFileError(Exception):
    pass

# the shapefile model

# Create your models here.
class Shp(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    shp_file = models.FileField(upload_to=uploaded_shp_files_relpath)
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

    instance_name = instance.name
    # it's going to be the same name we have in admin panel


    # it's the same password that we have in settings
    # conn_str = 'postgresql://postgres:password@localhost:5432/geoapp'

    print('shp_file: ', shp_file)
    print('file_name: ', file_name)
    print('file_format: ', file_format)
    print('file_path: ', file_path)

    if DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP:
        if "zip" in file_format:  # this is my idea to check that the uploaded file is a zip one
        # extract zipfile
            print("it's a zip")

            with zipfile.ZipFile(shp_file, 'r') as zip_ref:
                zip_ref.extractall(file_path)

            os.remove(shp_file) # remove zip file

        else:
            raise NotAZIPFileError("The shapefile given in input must be in zip format. It is {}".format(file_format))

    # Python glob. glob() method returns a list of files or folders that matches the path specified in the pathname argument.
    # https://pynative.com/python-glob/#:~:text=Python%20glob.,UNIX%20shell%2Dstyle%20wildcards).
    shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True) # to get shp, among the n files inside the zip
    # se il file è uno zip, devo usare il primo elemento della lista altrimenti il'uscita di glob.glob è una lista

    print(shp)

    try:
        req_shp = shp[0]

        gdf = gpd.read_file(req_shp)  # make geodataframe

        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema=schm_name,
            name=instance_name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)

        instance.delete()
        print("There is problem during shp upload: ", e)
    
    # req_shp = shp[0]

    # gdf = gpd.read_file(req_shp)  # make geodataframe


    # crs_name = str(gdf.crs.srs)

    # print('crs_name: ', crs_name)

    # epsg = int(crs_name.lower().replace('epsg:', ''))

    # if epsg is None:
    #     epsg=4326 # wgs84 coordinate system

    # geom_type = gdf.geom_type[1]

    # engine = create_engine(conn_str)  # create the SQLAlchemy engine to use

    # gdf['geom'] = gdf['geometry'].apply(lambda x: WKTElement(x.wkt, srid=epsg))

    # gdf.drop('geometry', 1, inplace=True)  # drop the geometry column since we already bckup this column with geom
    # # In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only.

    # # post gdf to the postgresql
    # # gdf.to_sql(file_name, engine, 'public', if_exists='replace', index=False, dtype={'geom': Geometry('Geometry', srid=epsg)})
    # # for the name of the tabel, I can now just put the name of the instance uploaded
    # gdf.to_sql(instance_name, 
    #            engine, 
    #            'public', 
    #            if_exists='replace', 
    #            index=False, 
    #            dtype={
    #                'geom': Geometry('Geometry', srid=epsg)
    #                }
    #             )

    '''
    publish shp to geoserver using geoserver-rest
    '''

    # check that the elements exists
    if not geo.get_workspace(wksp_name):
        print("create workspace '{}'".fomat(wksp_name))
        geo.create_workspace(wksp_name)


    # print("getting workspace:", geo.get_workspace(wksp_name))

    geo.create_featurestore(workspace=wksp_name, 
                            store_name=ste_name, 
                            schema=schm_name,
                            db=db_params['dbname'], 
                            host=db_params['host'], 
                            pg_user=db_params['user'], 
                            pg_password=db_params['password']
                            )
    # shapefile will be published in "data" schema
    print("create featurestore")
    # print(wksp_name, ste_name, schm_name, db_params['dbname'],db_params['host'],db_params['user'], db_params['password'])

    # geo.publish_featurestore(workspace=wksp_name, store_name=ste_name, pg_table=file_name)
    # for the name of the tabel, I can now just put the name of the instance uploaded
    geo.publish_featurestore(workspace=wksp_name, 
                             store_name=ste_name, 
                             pg_table=instance_name)
    print("publish featurestore")


    # edit style
    geo.create_outline_featurestyle(sty_name, 
                                    workspace=wksp_name)
    # the first argument is the output style name

    geo.publish_style(
        layer_name=layr_name, 
        style_name=sty_name, 
        workspace=wksp_name)
    print("publish style")


    # workspace si riferisce a geoserver-rest
    #  schema si rieferisce a pgadmin


@receiver(post_delete, sender=Shp)
def delete_data(sender, instance, **kwargs):
    # # the content of this class is somehow copied from venv/lib/site-package/geo/Postgres.py 
    # instance_name = instance.name

    # db.delete_table(
    #         instance_name,
    #         schema=schm_name
    #         ) 
    # # again, here i take directly the name of the uploaded instance
    
    # geo.delete_layer(instance_name, layr_name)

    # pass

    db.delete_table(instance.name, schema=schm_name)
    geo.delete_layer(instance.name, layr_name)