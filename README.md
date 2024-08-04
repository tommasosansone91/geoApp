# Web Mapping and Web-GIS from Dev to Deployment: GeoDjango

This django app allows the user to load `.tiff` files and zipped `.shp` files into `geoserver` software, where they are used as source to display their representation on the map of the frontend part of the app.

The upload can be done via the django-admin UI page.

The tiff file is directly loaded into geoserver, while the shp file is also loaded into postgres as table having name equal to the name specified in the upload UI panel.

## requirements

This app requires java 11 or 17, geoserver, postgres and postgis extension for postgres.

## original source of the code

### original repo name

    geodjango-from-dev-to-deployment

### verbose project name

    Web Mapping and Web-GIS from Dev to Deployment: GeoDjango


## refactored code

### project name

    geoApp

### django apps

    geoApp
    shp
    tiff
