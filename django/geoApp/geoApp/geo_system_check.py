import requests
from geoApp.exceptions import GeoserverNotRespondingError
from geoApp.geo_system_configs import GEOSERVER_URL

# hot to call it:
# check_geoserver_status()

def check_geoserver_status():
    print("Checking geoserver availability...")
    try:
        response = requests.get(GEOSERVER_URL)
        if response.status_code == 200:
            print("GeoServer is up and running!")
        else:
            print("GeoServer returned a non-200 status code: {}".format(response.status_code))
        return(response.status_code)
    
    except GeoserverNotRespondingError as e:
        print("Error connecting to GeoServer: {}".format(e))
        return(500)


