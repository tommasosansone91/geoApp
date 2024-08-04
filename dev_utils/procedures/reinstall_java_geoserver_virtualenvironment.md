# reinstall java, geoserver, virtal environment

In case you installed the wrong java version, you can follow this guideline to uninstall an reinstall java and the components based on it.


## uninstall old java


follow the staps indicatend in this tutorial https://askubuntu.com/a/185250/1342430

remove jdk .sh file

    sudo rm /etc/profile.d/jdk.sh

remove other java-related things

    locate jdk-18 | xargs rm -f

remove the geoserver default config file

    sudo rm /etc/default/geoserver


## uninstall geoserver

stop geoserver

    cd /usr/share/geoserver/bin
    sh shutdown.sh

simply remove the folder where it was installed

    cd /usr/share/
    sudo rm -r geoserver/


## remove the virtual environment

    cd ....

    source venv/bin/activate

    pip freeze > old_venv_requirements.txt

    deactivate

    rm -r venv



reinstall java 11 (doc of geoserver (not hte rest one!) says only java 17 or 11 will work)
----------------------------------------------------------------------------------------------
sudo apt update
sudo apt install openjdk-11-jdk


rifai il venv con i suoi componenti
--------------------------------------

cd /corsi_udemy/web-mapping-and-webgis-geodjango/geoserver-rest

virtualenv venv

source venv/bin/activate

sudo apt install libgdal-dev
pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

pip install -r requirements.txt




reinstall geoserver from documentation
----------------------------------------
https://docs.geoserver.org/latest/en/user/installation/linux.html

linux: select web archive from https://geoserver.org/release/stable/

downloaded
and saved into new path
cd /usr/share/
sudo mkdir geoserver

cp ..../geoserver-2.22.0-bin.zip  /usr/share/geoserver/

---> /usr/share/geoserver/geoserver-2.22.0-bin.zip

unzip via UI

cd /usr/share/geoserver/
xdg-open .

e.g. /usr/share/geoserver/lib/

run 
echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
. ~/.profile

sudo chown -R USER_NAME /usr/share/geoserver/
sudo chown -R tommaso /usr/share/geoserver/

cd /usr/share/geoserver/bin/ && sh startup.sh 

In a web browser, navigate to http://localhost:8080/geoserver


