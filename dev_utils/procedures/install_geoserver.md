# install geoserver

This guide explains how to install geoserver on the development machine.


## install java 11

>[!IMPORTANT] 
> doc of geoserver (not the rest one!) says only java 17 or 11 will work.

    sudo apt update
    sudo apt install openjdk-11-jdk


## install geoserver 

following the documentation https://docs.geoserver.org/latest/en/user/installation/linux.html

linux: select **"Platform Independent Binary"**

Platform Independent Binary is the link having this description
> Operating system independent runnable binary.

downloaded<br>
and saved into new path<br>

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

    sudo chown -R $USER /usr/share/geoserver/

e.g.

    sudo chown -R tommaso /usr/share/geoserver/

## test geoserver

    cd /usr/share/geoserver/bin/ && sh startup.sh 

wait some seconds, then, in a web browser, navigate to http://localhost:8080/geoserver


