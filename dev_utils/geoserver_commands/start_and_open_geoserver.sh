#!bin/bash

cd /usr/share/geoserver/bin
nohup sh startup.sh  &  # lo fa partire

time_to_wait="20s"

echo "wait $time_to_wait"
sleep $time_to_wait

xdg-open http://localhost:8080/geoserver