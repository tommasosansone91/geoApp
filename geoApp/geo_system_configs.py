
from geoApp.settings import DATABASES

from osgeo import gdal

from geoApp.utils import \
                        has_non_alphanumeric_characters, \
                        has_uppercase_characters

from django.core.exceptions import ValidationError

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
# psql -d geoappdb -U geoapp_main -h localhost

GEOSERVER_URL = "http://localhost:8080/geoserver/web"


# define proper elelments of geoserver
#----------------------------------------------

# these elements should be each turned into a model.
# the model should be filled with default elements at mingrations
# the form to insert new geodata should indicate allow to insert new geoserver rest elements or select from dropdown menu.

# the workspace is created once by user in geoserver UI
wksp_name = 'geoapp'

# store_name
ste_name = 'geoapp'

# schema name
schm_name = 'data'

# style name
sty_name = 'my_style' 


# variables validation
#-----------------------

geoserver_elements =  {
    
    "workspace_name": wksp_name,
    "schema_name": schm_name, 
    "store_name": ste_name,
    "style_name": sty_name,
}

for element in geoserver_elements:

    geoserver_element_is_valid = True

    if has_uppercase_characters(geoserver_elements[element]):
        geoserver_element_is_valid = False

    if has_non_alphanumeric_characters(geoserver_elements[element]):
        geoserver_element_is_valid = False


    if not geoserver_element_is_valid:
        raise ValidationError("Validation failed for geoserver element {}. Its value is '{}'. It is not valid.".format(element, geoserver_elements[element]))
