# create_engine

    # PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
    # RETURN THE SQLACHEMY ENGINE OBJECT
    def get_connection():
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            )
        )