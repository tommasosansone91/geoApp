# add new server to postgres via pgadmin

## add new server 

got to pgadmin on browser

http://localhost/pgadmin4/login?next=%2Fpgadmin4%2F

this service is started automatically with the OS

### new server credentials

name

    postgres-local

username

    postgres

pw
    
    postgres

hostname / address
    
    127.0.0.1

port
    
    5432

server group
    
    Servers

>[!NOTE] 
>this server is created by user `postgres`.
>Its password must be set to `postgres`, as this is default postgresql root user password

    sudo -i -u postgres
    psql

    ALTER USER postgres WITH PASSWORD 'postgres';


register your new pgadmin user with email and password

    email@email.com
    password

http://localhost/pgadmin4/login?next=%2Fpgadmin4%2F

default server is postgres

default schema is public

### create postgres extenstion to the database

#### method 1

    sudo -i -u postgres

    psql -d geoappdb

    CREATE EXTENSION postgis

#### method 2

from pgadmin toolbar

tool > query tool

    CREATE EXTENSION postgis

 
### check table spatial_ref_sys

refresh schema

    select * from spatial_ref_sys;

this table is created only if the extension was installed successfully


### create and fill in tables having geometry fields

    create table demo(
        id serial primary key,
        name text,
        geometric_field geometry
    );

    insert into demo(name, geometric_field)
    values('Point', ST_GeomFromText('Point(1 1)'));

    -- geometric query - can investigate it with geometry viewer
    select * from public.demo;