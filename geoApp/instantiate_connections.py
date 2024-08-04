

from geo.Geoserver import Geoserver

# from geo.Geoserver.Postgres import Db
# this one import from venv/lib/site-package/geo/Postgres.py where a Db class is defined
# this is deprecated. this module and class do not exist anymore.

from pg.pg import Pg  # postgres-helper library made by the course author

from geoApp.geo_system_configs import GEOSERVER_CREDENTIALS
from geoApp.geo_system_configs import geoapp_db_params


# initializations
#------------------

# initialize the Pg class
db = Pg(
    dbname=geoapp_db_params['dbname'], 
    user=geoapp_db_params['user'], 
    password=geoapp_db_params['password'], 
    host=geoapp_db_params['host'], 
    port=geoapp_db_params['port']
    )

# initialize the library
geo = Geoserver(
            'http://127.0.0.1:8080/geoserver', 
            username=GEOSERVER_CREDENTIALS['user'], 
            password=GEOSERVER_CREDENTIALS['password']
            )
#aligned

# the connection string is created on base of db params defined in settins.py, 
conn_str = 'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format( **geoapp_db_params )


# health check of geoserver


print(
"""
credentials:
-------------

geoapp_db_params
{}

GEOSERVER_CREDENTIALS: 
{}

conn_str: 
{}

      
""".format(geoapp_db_params, GEOSERVER_CREDENTIALS, conn_str)
)
