
from geoApp.settings import DATABASES

from osgeo import gdal

# handle gdal exceptions
#----------------------------------------

gdal.UseExceptions()    # Enable exceptions
# gdal.DontUseExceptions()


# define variables
#-------------------

GEOSERVER_CREDENTIALS = {
    'user': 'admin',
    'password': 'geoserver'
}

# reorganizarion of database credentials
geoapp_db_params = {
        'user':     DATABASES['default']['USER'],
        'password': DATABASES['default']['PASSWORD'],
        'host':     DATABASES['default']['HOST'],
        'port':     DATABASES['default']['PORT'],
        'dbname':   DATABASES['default']['NAME'],    
}
# psql -d geoapp -U postgres -h localhost

GEOSERVER_URL = "http://localhost:8080/geoserver/web"


# define proper elelments of geoserver
#----------------------------------------------

# these elements should be each turned into a model.
# the model should be filled with default elements at mingrations
# the form to insert new geodata should indicate allow to insert new geoserver rest elements or select from dropdown menu.

# the workspace is created once by user in geoserver UI
wksp_name = 'my_workspace'

# store_name
ste_name = 'my_store_name'

# schema name
schm_name = 'data'

# style name
sty_name = 'my_style' 


# variables validation
#-----------------------
