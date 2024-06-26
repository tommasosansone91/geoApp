import os

from geoApp.settings import UPLOADED_FILES_DIR

UPLOADED_SHP_FILES_DIR = 'shp'

import datetime

def generate_current_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, '%Y/%m/%d')
# uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, generate_current_timestamp())
uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR)

