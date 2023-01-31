

# usage
# -----------

# folloiwng https://pypi.org/project/geoserver-rest/

# launch this script by  
# python geoserver-rest.py

# Import the library
from geo.Geoserver import Geoserver

# Initialize the library
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='geoserver')

# devo tenere aperta una finestra web su geoserver.
# geoserver va startato
# devi loggarti con user e pw



# geo.create_workspace('demo')
# crea workspace accessibile dall ainterfaccia da menu di sx
# workspaces > demo

# lo lancio solo unavolta

# For uploading raster data to the geoserver
# this is from the tutoril pypi
# but I have chnged the key name layer_name and its value to raster1
# because I want to upload file raster1 in data folder of this project
geo.create_coveragestore( layer_name='raster1', path=r'data/raster/raster1.tif', workspace='demo')

# dopo questo lancio python geoserver-rest.py

# vedo il suo risultato in workpaces dell'intefaaccia di geoserver
# poi vaod nella tb layerpreview
# e vedo il layer raster1

# con openlayers della ui posso visualozzare i dati

# create featurestore
#----------------------

# per importare ed esportare i metadata feature json data usiamo il manager di postgis che apor dalla barra di comando
# postgis shapefile import export manager

geo.create_featurestore(store_name='geo_data', workspace='demo', db='postgres', host='localhost', pg_user='postgres',
                        pg_password='admin')
geo.publish_featurestore(workspace='demo', store_name='geo_data', pg_table='geodata_table_name')
