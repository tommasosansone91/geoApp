# run apps manually

## django

    # start geoserver

    cd ~/tommaso03/coding_projects/corsi_udemy/web-mapping-and-webgis-geodjango
    bash dev_utils/geoserver_commands/start_and_open_geoserver.sh


    # activate virtual environments

    deactivate
    cd ~/tommaso03/coding_projects/corsi_udemy/web-mapping-and-webgis-geodjango
    source django/venv/bin/activate

    # run app

    cd django/geoApp
    python manage.py runserver


### Test the django app

    python manage.py test shp

    python manage.py test tiff
    

## geoserver-rest

    deactivate

    cd ~/tommaso03/coding_projects/corsi_udemy/web-mapping-and-webgis-geodjango

    source geoserver-rest/venv/bin/activate

    cd geoserver-rest

    python geoserver-rest.py