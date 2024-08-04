

# usage
# -----------

# folloiwng https://pypi.org/project/geoserver-rest/

#  activate the venv
# source venv/bin/activate

# activate geoserver
# cd /usr/share/geoserver/bin/ && sh startup.sh 

# launch this script by  
# python geoserver-rest-2.py

# Import the library
from geo.Geoserver import Geoserver



# Initialize the library : istanziare un geoserver
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='geoserver')




wksp_name='geoapp'

# store_name
ste_name='geoApp'

# schema name
schm_name = 'data'

# style name
sty_name = 'geoApp_shp_style'


# create featurestore
#----------------------

# per importare ed esportare i metadata feature json data usiamo il manager di postgis che apor dalla barra di comando
# postgis shapefile import export manager

# we want to publish the layer, so we use createfeaturestore.
# prima lo creo, poi lo pubblico

geo.create_featurestore(store_name='postgis', workspace='demo', db='postgres', host='localhost', pg_user='postgres', pg_password='password')

        # geo.create_featurestore(workspace=wksp_name, 
        #                         store_name=ste_name, 
        #                         schema=schm_name,
        #                         db=geoapp_db_params['dbname'], 
        #                         host=geoapp_db_params['host'], 
        #                         pg_user=geoapp_db_params['user'], 
        #                         pg_password=geoapp_db_params['password']
        #                         )

geo.publish_featurestore(workspace='geoapp', store_name='postgis', pg_table='jamoat-db-2')

        # geo.publish_featurestore(workspace=wksp_name, 
        #                         store_name=ste_name, 
        #                         pg_table=instance_name)

# now i want to apply a style to the uploaded raster file.
# styles are file which are part of the group of a shapefile.
# this upload the stile to the db, in the workspace, i can see it in geoserver in style tab
# http://localhost:8080/geoserver/web/wicket/bookmarkable/org.geoserver.wms.web.data.StylePage?5&filter=false




