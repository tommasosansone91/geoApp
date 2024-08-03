#!/bin/bash

# this file will be triggered by the cron and launch the BaseCommand to store data into the database.

cd /var/www/geoApp

# source venv/bin/activate
# it is not needed since I specify the python interpreter from the venv in the next line


venv/bin/python manage.py save_current_pm_values_in_history


venv/bin/python manage.py arrange_historical_and_daily_series
