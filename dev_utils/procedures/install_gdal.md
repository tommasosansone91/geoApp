# install GDAL

This is to explain how to install the python library GDAL inside any virtual environment.

    virtualenv venv

    source venv/bin/activate

    sudo apt install libgdal-dev

    cat requirements.txt | xargs -n 1 pip install

    pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

>[!IMPORTANT]
> the python library of GDAL must have version corresponding to the GDAL installed via apt-get

>[!IMPORTANT]
> the python library of GDAL cannot get installed if `libgdal-dev` is not already been installed via `apt-get`.

> [!NOTE]  
> Both the django app and the standalone geoserver-rest script require GDAL.