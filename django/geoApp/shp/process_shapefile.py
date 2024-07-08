

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

from shp.configs import DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP
from shp.configs import UPLOADED_SHP_FILES_MUST_BE_ZIPPED


from geoApp.geo_system_configs import geoapp_db_params

from shp.configs import \
                        wksp_name,  \
                        ste_name,   \
                        schm_name,  \
                        layr_name,  \
                        sty_name    \
                        

from geoApp.exceptions import \
                        NotAZipFileError,           \
                        NotAShapefileError,         \
                        NoShapeFileFoundError,      \
                        TooManyShapeFileFoundError  \

from geoApp.instantiate_connections import \
                                        geo,        \
                                        db,         \
                                        conn_str    \


def publish_shp_geo_data(instance):
        print("publish_shp_geo_data function - ACTIVATES - Instance: {}".format(instance))

        shp_file_abspath = instance.shp_file.path
        file_name = os.path.basename(shp_file_abspath)
        file_format = os.path.basename(shp_file_abspath).split('.')[-1]
        file_name_noext = os.path.basename(shp_file_abspath).split('.')[0]  # without the format
        shp_file_folder_abspath = os.path.dirname(shp_file_abspath)

        instance_name = instance.name
        # it's going to be the same name we have in admin panel

        # print('shp_file_abspath: ', shp_file_abspath)
        # print('file_name: ', file_name)
        # print('file_name_noext: ', file_name_noext)
        # print('file_format: ', file_format)
        # print('shp_file_folder_abspath: ', shp_file_folder_abspath)

        if DETECT_AND_UNZIP_LOADED_ZIPFILE_IN_SHP:
            if "zip" in file_format:  # this is my idea to check that the uploaded file is a zip one
            # extract zipfile
                print(
                    "The uploaded file {} is a zip file!\nExtracting its content of  in folder {}".format(
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

        # print(shp_files_list)

        if len(shp_files_list) == 0:
            raise NoShapeFileFoundError("No shapefile found.")

        if len(shp_files_list) > 1:
            raise TooManyShapeFileFoundError("Too many shapefile found.")
        
        try:
            req_shp = shp_files_list[0]
            print("Detected shapefile: {}".format(req_shp))

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

            print("Instance {} was sent to_postgis!".format(instance_name))

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

        # this does not work


        # edit style
        geo.create_outline_featurestyle(sty_name, 
                                        workspace=wksp_name)
        # the first argument is the output style name

        geo.publish_style(
            layer_name=layr_name, 
            style_name=sty_name, 
            workspace=wksp_name)
        
        print("published style {} for layer {}".format(sty_name, layr_name))

        # tested: style is published

        # workspace si riferisce a geoserver-rest
        #  schema si rieferisce a pgadmin