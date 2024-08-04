

# usage
# -----------

# folloiwng https://pypi.org/project/geoserver-rest/

#  activate the venv
# source venv/bin/activate

# activate geoserver
# cd /usr/share/geoserver/bin/ && sh startup.sh 

# launch this script by  
# python geoserver-rest.py

# Import the library
from geo.Geoserver import Geoserver



# Initialize the library : istanziare un geoserver
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='geoserver')

# devo tenere aperta una finestra web su geoserver.
# geoserver va startato
# devi loggarti con user e pw

# start anew workspace each time - every object attached to it would be deleted in cascade ?
geo.delete_workspace(workspace='demo')

geo.create_workspace('demo')
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

# we want to publish the layer, so we use createfeaturestore.
# prima lo creo, poi lo pubblico

geo.create_featurestore(store_name='postgis', workspace='demo', db='postgres', host='localhost', pg_user='postgres', pg_password='password')

geo.publish_featurestore(workspace='demo', store_name='postgis', pg_table='jamoat-db')

# now i want to apply a style to the uploaded raster file.
# styles are file which are part of the group of a shapefile.
# this upload the stile to the db, in the workspace, i can see it in geoserver in style tab
# http://localhost:8080/geoserver/web/wicket/bookmarkable/org.geoserver.wms.web.data.StylePage?5&filter=false

# carico raster1.tif dai data in qgis

geo.upload_style(path='data/style/custom_style1_raster1.sld', workspace='demo')

geo.upload_style(path='data/style/raster1.sld', workspace='demo')

#  now i publish the style
geo.publish_style(layer_name='raster1', style_name='raster1', workspace='demo')

# now i create coverage style
# the name i give to the style is raster-new, i will see it in thestyle tab of geoserver UI
geo.create_coveragestyle(raster_path='data/raster/raster1.tif', style_name='raster-new', workspace='demo', color_ramp='hsv')


#  now i publish the style
geo.publish_style(layer_name='raster-new', style_name='raster1', workspace='demo')


geo.create_outline_featurestyle('polygon-style', workspace='demo')
geo.publish_style(layer_name='jamoat-db', style_name='polygon-style', workspace='demo')