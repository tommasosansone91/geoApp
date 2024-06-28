import os
import datetime

# from geoApp.settings import UPLOADED_FILES_DIR
from geoApp.settings import DATABASES


def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%_H%M%S")

def generate_uploaded_shp_file_relpath():

    UPLOADED_SHP_FILES_DIR = 'shp'
    uploaded_shp_files_relpath_from_media_root = UPLOADED_SHP_FILES_DIR

    # name = instance.name.replace(" ", "_").replace("-", "_").lower()
    timestamp = generate_current_timestamp()

    # name of the folder which will contain the uploaded file
    # current_file_subfolder = name +  "_" + timestamp
    current_file_subfolder = timestamp

    # relative path of the folder which will contain the uploaded file
    uploaded_shp_file_relpath = os.path.join(
        uploaded_shp_files_relpath_from_media_root,  
        current_file_subfolder
        )

    # print("generated new uploaded_shp_file_relpath: {}".format(uploaded_shp_file_relpath) )

    return uploaded_shp_file_relpath


# uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, '%Y/%m/%d')
# uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, generate_current_timestamp())







# define proper elelments of geoserver
#----------------------------------------------

# the workspace is created once by user in geoserver UI
wksp_name='geoapp'

# store_name
ste_name='geoApp'

# schema name
schm_name = 'data'

# layer name
layr_name = 'geoapp'

# style name
sty_name = 'geoApp_shp_style'
