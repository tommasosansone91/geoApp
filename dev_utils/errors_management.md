# errors management

    from geo.Geoserver.Postgres import Db

    ModuleNotFoundError: No module named 'geo.Geoserver.Postgres'; 'geo.Geoserver' is not a package

nell'ultima versione di geo non c'è la classe Db.

devo prendere invece


    from pg.pg import Pg

    # initialize the Pg class

    db = Pg(
        dbname=db_params['dbname'], 
        user=db_params['user'], 
        password=db_params['password'], 
        host=db_params['host'], 
        port=db_params['port']
        )

this requires pip installing pymongo and postgres-helper