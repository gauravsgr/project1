import psycopg2
try:
    connection = psycopg2.connect(user = "msobihnqxyumrq",
                                  password = "b03ed56794ebf47d1964a2a894928421cfa54789cf5de8758d83195a4ec078d4",
                                  host = "ec2-107-21-97-5.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "dbli7nj2hicob8")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")