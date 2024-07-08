
from geoApp.settings import DATABASES

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



# variables validation
#-----------------------
