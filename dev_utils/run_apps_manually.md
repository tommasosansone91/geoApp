# run apps manually

This is to run the app on the development machine.

## django

    # start geoserver

    cd ~/tommaso03/coding_projects/corsi_udemy/geoApp
    bash dev_utils/geoserver_commands/start_and_open_geoserver.sh


    # activate virtual environments

    deactivate
    cd ~/tommaso03/coding_projects/corsi_udemy/geoApp
    source /venv/bin/activate

    # run app

    python manage.py runserver


### Test the django app

    python manage.py test shp

    python manage.py test tiff
    

## geoserver-rest

    deactivate

    cd ~/tommaso03/coding_projects/corsi_udemy/geoApp

    source geoserver-rest/venv/bin/activate

    cd geoserver-rest

    python geoserver-rest.py