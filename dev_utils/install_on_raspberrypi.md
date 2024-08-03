# Install on Raspberry pi

This procedure gives instructions on how to install the app geoApp on a Raspberry pi.

> [!IMPORTANT]
> The Raspberry pi and the PC used for the deploy must be connected to the same LAN network.


## Key exchange between RPi and github

from your PC log into the RPi.

    ssh pi@<RPi_IP>

    <RPi_user_pi_password>

become admin

    sudo su

    ssh-keygen -t ed25519 -C "your_mail_address@your_dominion.it"

press <kbd>enter</kbd>

> [!IMPORTANT]
> This password becomes the password you have to give in from the RPi to interact with github (e.g. `git clone`), so note it down..

    <RPi_git_password>

    <RPi_git_password>

output:

    Generating public/private ed25519 key pair.
    Enter file in which to save the key (/root/.ssh/id_ed25519): 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /root/.ssh/id_ed25519.
    Your public key has been saved in /root/.ssh/id_ed25519.pub.
    The key fingerprint is:

    ...

activate the ssh agent

    eval $(ssh-agent -s)

this should return

>    Agent pid 716

add the new .ssh file to the files recognized by the ssh agent

    ssh-add ~/.ssh/id_ed25519

    <RPi_git_password>

get the content of the file ending with `.pub`

    cat ~/.ssh/id_ed25519.pub

copy the output of this command (it should start with `ssh-ed25519 ` and end with the e-mail address)

log in into your github account and go to

https://github.com/settings/ssh/new

> github profile > top-right dropdown menu > settings > left-side menu > SSH and GPG keys > add ssh key

> [!TIP]
> Choose a self-explanatory title, such as 
> `id_ed25519.pub_from_RPi_model4B_4GB`
> so that you will remember which device it is associated to.


## Clone the app on raspberry pi

from your PC log into the RPi.

    ssh pi@<RPi_IP>

    <RPi_git_password>

become admin

    sudo su


### Install git

    sudo apt update
    sudo apt install git


### clone the app

Go to the directory where we want to install the app

    cd /var/www/

get the git clone link from github:

- go to the github repo
- `Code` button
- `HTTPS` tab
- copy the link

> [!IMPORTANT]
> On deploy machine, git clone the project by using the github link starting with `https`. 
> This one allows to pull the project easily (but it should not allow the user to push changes to github, so it is safer).<br>
> On development, git clone the project by using the github link starting with  `git@`.
> This one allows to git push the project easily by using github SSH authentication method (SSH key exchange between github and the machine).

    git clone https://github.com/tommasosansone91/geoApp.git


## Install Nginx as web server and reverse proxy

This is the *web server* (server the static files) and *reverse proxy* (forwards the dynamic requests to Django).

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    apt-get update
    apt-get install nginx

test that it works by running

    hostname -I

then place in your browser the URL

    http://<RPi_IP>

you should see the Nginx welcome page.

**NOTE:** Nginx configuration will be done later.


## Install Postgresql database

### Install

    sudo apt-get update
    sudo apt-get install postgresql

Check the port on which postgres is listening

    sudo netstat -lntp | grep postgres


### Reset root default password

Useful information for Ubuntu: https://askubuntu.com/a/1466769/1342430

Useful information for AWS EC2: https://www.qunsul.com/posts/installing-postgresql-13-on-ubuntu-ec2-instance.html

The default password for postgresql is `postgres`, but it is better to change it for security reasons.

Become user `postgres`

    sudo -i -u postgres

open the postgres shell

    psql

reset the root password

    \password postgres

> [!CAUTION]
> This will become the new root password of postgres.
> If you forget this, you will not be able to manage postgresql anymore, so **note it down**.

    rootpassword

    rootpassword

commit the change by exiting the shell

    exit


### Create a new database for the app

enter the postgres shell as `postgres` user

    psql -h localhost -U postgres -d postgres

create the new database

    create database geoappdb;

create a "main" and a "readonly" user for the app

    create user geoapp_main WITH ENCRYPTED PASSWORD 'geomain';  # choose short one

    create user geoapp_readonly WITH ENCRYPTED PASSWORD 'georeadonly';  # choose short one

make the main user the owner of the database

    alter database geoappdb OWNER TO geoapp_main;


#### Test the database connection

exit the shell and test to reopen it as the "main user of the app"

    exit

    psql -h localhost -U geoapp_main -d geoappdb


> [!IMPORTANT]
> The database name, the database-owner user and its password become the credentials for the Django app to access the database.

    'NAME': 'geoappdb',
    'USER': 'geoapp_main',
    'PASSWORD': 'geomain',

These credentials must be inserted in the `DATABASES` variable in `settings.py` module of the Django main app (the one created by default by django, at the same folder level of the other django apps inside that Django project).

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<db name here>',
            'USER': '<user here>',
            'PASSWORD': '<password here>',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


#### Install postgis extension inside the geoappdb database

    sudo -i -u postgres

    psql -d geoappdb

    CREATE EXTENSION postgis;

    exit


#### create a new schema inside the geoappdb database

    psql -h localhost -U geoapp_main -d geoappdb

    create schema data;

    exit


## install geoserver

This app requires the software geoserver to be installed and running.

geoserver requires java to be installed.


### install java 11

>[!IMPORTANT] 
> doc of geoserver (not the rest one!) says only java 17 or 11 will work.

    sudo apt update
    sudo apt install openjdk-11-jdk


### install geoserver 

following the documentation https://docs.geoserver.org/latest/en/user/installation/linux.html

linux: select web archive from https://geoserver.org/release/stable/

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


### test geoserver

    cd /usr/share/geoserver/bin/ && sh startup.sh 

wait some seconds, then, in a web browser, navigate to http://localhost:8080/geoserver


## Install Python

    sudo add-apt-repository ppa:deadsnakes/ppa

    sudo apt update

> [!WARNING]
> Do not install a different version of python3.
> Compatibility between Python 3.8 and the content of the requirements.txt file, ovarall Django 3.1.4, is guaranteed by the author.

    sudo apt install python3.8


## Install pip and virtualenv

    sudo apt-get install pip

    sudo apt install python3-virtualenv


## create virtual environment

> [!NOTE]
> This procedure is to create a virtual environment on the deploy machine, the RPi.<br>
> To create the virtual environment on the development machine, just run `python3 -m venv ./venv/` .<br>
> Syntax: `python3 -m venv ./<virtual_environment_name>/`

    sudo su

    cd /var/www/geoApp

specifically use python3 to create a virtual environment for the app in folder `venv`

    /usr/local/opt/python-3.8.1/bin/python3.8 -m venv ./venv/

ativate and deactivate the virtual environment only for testing

    source venv/bin/activate
    deactivate


## Install the python modules

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

> [!WARNING]
> Make sure you have already installed postgresql, or the installation of python module `psycopg2` will raise problems and confliects.

    sudo apt update


### Safe install of GDAL

safe install `GDAL` before massively installing all the other python modules.

GDAL can be installed as python module only if it was before installed "at OS-level" (via `apt`).

    sudo apt install libgdal-dev

Install GDAL as python module

    pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

>[!IMPORTANT]
> the python library of GDAL must have version corresponding to the GDAL installed via apt.


### Safe install of psycopg2

safe install `psycopg2` before massively installing all the other python modules

    pip install psycopg2-binary

**only if it does not work again**, run

    sudo apt-get install libpq-dev

Once `psycopg2` is installed, launch the massive safe installation of required python modules


### Massive install of python modules in requirements.txt

    cat requirements.txt | xargs -n 1 pip install

for every package which raises problems, open the file `requirements.txt`, look up for the line including that module and remove the string `==X.X.X`, then run again the same command

    cat requirements.txt | xargs -n 1 pip install


### Safely reinstall GDAL correct version

    pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

>[!TIP]
> the python library of GDAL must have version corresponding to the GDAL installed via apt.


## Create the app tables in postgresql via python

Once the app framework and postgres are both installed, create the tables required by the app to operate correctly.

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    python manage.py makemigrations

    python manage.py migrate


## Create superuser

Create superuser in order to access the admin section of the app.

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    python manage.py createsuperuser


## Collect static files

Custom static files (images, javascript and css - i.e. everything useful for beautifying the frontend) are developed in the static folders defined in the list variable `STATICFILES_DIRS` in settings.<br>
In this app, one of these flders is is `static`.

In production (i.e. when `DEBUG = False`), the static files must be served by the web server (e.g. nginx).

Since the layout of the admin section (and eventually some third-parts django libraries) is managed by Django, the static files of the admin section will automatically created into the folder defined in the variable `STATIC_ROOT` in settings.<br>
In this app it is `staticfiles`.

So, every time new static files are developed in `STATICFILES_DIRS` folders, the `STATIC_ROOT` folder must be updated.<br>
This can be done by running the django command `collectstatic`.

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    python manage.py collectstatic   


## Configure the app to be hosted on the RPi

In `geoApp/settings.py`, insert the IP of the RPi in the list variable `ALLOWED_HOSTS`

    ALLOWED_HOSTS = ['<RPi_IP>']

or leave it to

    ALLOWED_HOSTS = ['*']

to allow the app to be hosted on any server (not recommanded for security reasons).

In the end, test that the app can be on the RPi without throwing any error.

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    python manage.py runserver 0.0.0.0:8001


## Configure Nginx to serve the app

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

the default nginx configuration files are at paths

    /etc/nginx/sites-enabled/default
    /etc/nginx/sites-available/default

but we do not need the one in `sites-enabled`, so you can delete it

    rm /etc/nginx/sites-enabled/default

Create the symbolic link

    ln -s /var/www/geoApp/infrastructure/nginx/geoApp_nginx.conf /etc/nginx/conf.d/

Check that the symbolic link is right, run 

    ll /etc/nginx/conf.d

you should see

    lrwxrwxrwx 1 root root   68 May  5 21:18 geoApp_nginx.conf -> /var/www/geoApp/infrastructure/nginx/geoApp_nginx.conf


This allows Nginx to find the app-specific configuration file `infrastructure/nginx/geoApp_nginx.conf` when it searches for configuration files.


### Check that Nginx is working

In case the app is running because it was manually started via `python manage.py runserver 0.0.0.0:8001`,
stop it via <kbd>ctrl</kbd> + <kbd>D</kbd>.

restart nginx

    /etc/init.d/nginx restart

By using the browser of any other device (other than the RPi) connected to the LAN network,<br>
connect via browser to both IP addresses

    http://<RPi_IP>
    http://<RPi_IP>:PORT_1  # e.g. the port of another app already running and exposed on the RPi
    http://<RPi_IP>:3001

**NOTE:** Make sure the prefix is **`http`** and not **`https`**.

The other app should still be reachable, while on port `http://<RPi_IP>:3001` you should get `502 bad gateway`, as the HTTP WSGI server for is not installed yet.

in case of errors, to rollback to the previous configuration, run

    sudo su
    cd /etc/nginx/conf.d/
    rm /etc/nginx/conf.d/geoApp_nginx.conf

    systemctl stop nginx.service
    systemctl start nginx.service
    systemctl status nginx.service

## web server for python: gunicorn

Gunicorn is an HTTP WSGI server (Web Server Gateway Interface) for Python applications. <br>
In other words, it is a web server designed to run Python web applications that adhere to the WSGI standard.


### install gunicorn

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    pip install gunicorn



### check you have wsgi file

> [!NOTE]
> Gunicorn requires that you have the .wsgi files in the root directory of your project , and **it will not be able to read it if it is elsewhere**.

The files in the app folder `infrastructure/wsgi/` must be symbolically linked into the root directory of the project.

    /var/www/geoApp/

Run

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate 

Create the symbolic link

    ln -s /var/www/geoApp/infrastructure/wsgi/geoApp.wsgi /var/www/geoApp/

Check that the symbolic link is right, run 

    ll /var/www/geoApp/

you should see the symbolic link and check that it is not colored in red

    lrwxrwxrwx  1 root root   74 May  5 15:26 geoApp.wsgi -> /var/www/geoApp/infrastructure/wsgi/geoApp.wsgi


### run the app manually via gunicorn

This command is to have Gunicorn running the python app.<br>
It binds the app **internal** port (8001) on which the app is exposed by the command `python manage.py runserver localhost:8001`, to the address and port `localhost:8001`.<br>
The `--bind` part tells Gunicorn that it has to listen HTTP requests coming from that port (from the app).

    sudo su
    cd /var/www/geoApp
    source venv/bin/activate

    PYTHONPATH=`pwd`/.. venv/bin/gunicorn geoApp.wsgi:application --bind localhost:8001

See here why PYTHONPATH=\`pwd\`/.. is required at the start of the line.

https://stackoverflow.com/a/39461113/7658051

By using the browser of any other device (other than the RPi) connected to the LAN network, you should see the app running at

http://192.168.1.106:3001/


### Start the app manually in background via gunicorn (and gracefully exit the machine)

> [!NOTE]
> This is just a temporary command and should be launched only to check that guincorn can run the app successfully.
> The starting, stopping and starting-at-boot of the app should be managed via systemd and the systemctl syntax, which should be implemented as last step of the app installation process.

    sudo su
    cd /var/www/geoApp/
    source venv/bin/activate

    sudo nohup env PYTHONPATH=`pwd`/.. venv/bin/gunicorn geoApp.wsgi:application --bind localhost:8001 > /home/pi/geoApp.log 2>&1 &


#### check that the app is up and running

    echo "Grepping the app name from ps aux"
    echo "$(ps aux | grep 'geoApp')"


#### exit the machine gracefully

> [!IMPORTANT]
> Do not use the X button of the UI of the terminal.

To exit the RPi gracefully, press <kbd>ctrl</kbd> + <kbd>D</kbd>

By using the browser of any other device (other than the RPi) connected to the LAN network, you should see the app still running at

http://192.168.1.106:3001/


## cron files

The files in the app folder `infrastructure/cron/` must be symbolically linked into directory

    /etc/cron.d/

of the RPi. 

Run

    sudo su
    cd /var/www/geoApp/
    source venv/bin/activate
    
Create the symbolic link

    ln -s /var/www/geoApp/infrastructure/cron/geoApp-cron /etc/cron.d/

Check that the symbolic link is right, run

    ll /etc/cron.d/geoApp-cron

you should see

    lrwxrwxrwx 1 root root 46 May  1 10:59 /etc/cron.d/geoApp-cron -> /var/www/geoApp/infrastructure/cron/geoApp-cron

This allows cron to find the app-specific cron file `infrastructure/cron/geoApp-cron` .

**NOTE:**
No `chmod` of the cron files is needed.<br>
No restart of cron is needed.

Just enable the execution of the files target of the cron

    sudo chmod +x infrastructure/sh/*


## Log files

Create directrory to host logs

    sudo mkdir /var/log/geoApp/


## Turn the app into a service

The files in the app folder `infrastructure/systemd/` must be symbolically linked into directory

    /etc/systemd/system 
    /etc/systemd/system/multi-user.target.wants/

of the RPi.

The first one will allow them to be run as services via the command `systemctl`.

The second one will allow them to be automatically started as service as the machine re/boots.

Run

    sudo su
    cd /var/www/geoApp/
    source venv/bin/activate

Create the symbolic links

    ln -s /var/www/geoApp/infrastructure/systemd/geoApp.service /etc/systemd/system/
    ln -s /var/www/geoApp/infrastructure/systemd/geoApp.service /etc/systemd/system/multi-user.target.wants/

Check that the symbolic link is right, run

    ll /etc/systemd/system/multi-user.target.wants/geoApp.service
    ll /etc/systemd/system/geoApp.service

you should see

    lrwxrwxrwx 1 root root 52 May  1 11:04 /etc/systemd/system/multi-user.target.wants/geoApp.service -> /var/www/geoApp/infrastructure/systemd/geoApp.service
    
    lrwxrwxrwx 1 root root 52 May  1 11:04 /etc/systemd/system/geoApp.service -> /var/www/geoApp/infrastructure/systemd/geoApp.service

start the service 

    sudo systemctl start geoApp.service

and check it is allright

    sudo systemctl status geoApp.service

To make this service automatically run on boot

    sudo systemctl daemon-reload
    sudo systemctl enable geoApp.service
    sudo systemctl restart geoApp.service  # there is no real need to run this

In the end, test that the service works after the RPi booting

> [!CAUTION]
> This will restart your RPi.

    sudo reboot

After a while, by using the browser of any other device (other than the RPi) connected to the LAN network, you should see the app automatically booted and running at

http://192.168.1.106:3001/

<hr>

In case you want to disable the program on boot

    sudo systemctl daemon-reload
    sudo systemctl disable geoApp.service

Documentation https://www.freedesktop.org/software/systemd/man/systemd.service.html

<hr>

In case you change nginx or wsgi configurations, reload the daemon and restart the services to make them effective

    /etc/init.d/nginx restart
    sudo systemctl daemon-reload
    sudo systemctl restart geoApp.service

<hr>

```diff
+ The app geoApp is now successfully installed!
```