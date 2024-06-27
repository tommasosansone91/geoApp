# install GDAL

the python library of GDAL must have version corresponding to the GDAL installed via apt-get

    sudo apt install libgdal-dev

    cat requirements.txt | xargs -n 1 pip install

    pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')


