

import geopandas as gpd

import os
import zipfile

import glob

# from sqlalchemy import Geometry, WKTElement
from sqlalchemy import *

# from geo.Geoserver.Postgres import Db
# this one import from venv/lib/site-package/geo/Postgres.py where a Db class is defined
# this is deprecated. this module and class do not exist anymore.



from geoApp.geo_system_configs import geoapp_db_params

from geoApp.geo_system_configs import \
                        wksp_name,  \
                        ste_name,   \
                        schm_name


from geoApp.instantiate_connections import \
                                        geo,        \
                                        db,         \
                                        conn_str    \


def publish_tiff_geo_data(instance):
        print("publish_tiff_geo_data function - ACTIVATES - Instance: {}".format(instance))

        tiff_file_abspath = instance.tiff_file.path
        # file_name = os.path.basename(tiff_file_abspath)
        # file_format = os.path.basename(tiff_file_abspath).split('.')[-1]
        # file_name_noext = os.path.basename(tiff_file_abspath).split('.')[0]  # without the format
        # tiff_file_folder_abspath = os.path.dirname(tiff_file_abspath)

        instance_name = instance.name
        # it's going to be the same name we have in admin panel

        # print('tiff_file_abspath: ', tiff_file_abspath)
        # print('file_name: ', file_name)
        # print('file_name_noext: ', file_name_noext)
        # print('file_format: ', file_format)
        # print('tiff_file_folder_abspath: ', tiff_file_folder_abspath)



        '''
        publish tiff to geoserver using geoserver-rest
        '''

        # check that the elements exists
        if not geo.get_workspace(wksp_name):
            print("create workspace '{}'".format(wksp_name))
            geo.create_workspace(wksp_name)


        # print("getting workspace:", geo.get_workspace(wksp_name))

        geo.create_coveragestore(tiff_file_abspath,
                                workspace=wksp_name, 
                                layer_name=instance_name,
                                )
        # tifffile will be published in "data" schema
        print("tiff\n\tcreated coveragestore:\n\ttiff layer name: {}\n\ttiff file path: {}".format(instance_name, tiff_file_abspath))
        # print(wksp_name, ste_name, schm_name, geoapp_db_params['dbname'],geoapp_db_params['host'],geoapp_db_params['user'], geoapp_db_params['password'])



        # edit style
        geo.create_coveragestyle(
                                tiff_file_abspath,
                                style_name=instance_name,
                                workspace=wksp_name
                                )
        # the first argument is the output style name

        print("tiff:\n\tcreated coveragestyle:\n\ttiff layer name: {}\n\ttiff file path: {}".format(instance_name, tiff_file_abspath))
        

        geo.publish_style(
            layer_name=instance_name, 
            style_name=instance_name, 
            workspace=wksp_name
            )
        
        print("tiff:\n\tpublished style '{}' for tiff layer '{}'".format(instance_name, instance_name))

        # tested: style is published

        # workspace si riferisce a geoserver-rest
        #  schema si rieferisce a pgadmin