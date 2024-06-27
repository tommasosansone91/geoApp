import os
import datetime

from geoApp.settings import UPLOADED_FILES_DIR
from geoApp.settings import DATABASES


def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

UPLOADED_SHP_FILES_DIR = 'shp'

# uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, '%Y/%m/%d')
# uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, generate_current_timestamp())
uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR)


# so I don't have to hardcode credentials but just to import them form only one place: settings.py
db_params = {
        'user':     DATABASES['default']['USER'],
        'password': DATABASES['default']['PASSWORD'],
        'host':     DATABASES['default']['HOST'],
        'port':     DATABASES['default']['PORT'],
        'dbname':   DATABASES['default']['NAME'],    
}


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
