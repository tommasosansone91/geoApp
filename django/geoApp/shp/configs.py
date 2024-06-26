import os

from geoApp.settings import UPLOADED_FILES_DIR

UPLOADED_SHP_FILES_DIR = 'shp'

uploaded_shp_files_relpath = os.path.join(UPLOADED_FILES_DIR, UPLOADED_SHP_FILES_DIR, '%Y/%m/%d')

