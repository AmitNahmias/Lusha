CSV_DB_PATH = '/Users/amitnahmias/Documents/Lusha/caller_id_db.csv'
DRIVER_PATH = '/Users/amitnahmias/Documents/Lusha/postgresql-42.7.2.jar'
DB_NAME = 'postgres'
DB_CONF = \
    {
        "user": "postgres",
        "password": "12345678",
        "driver": "org.postgresql.Driver",
        "url": f"jdbc:postgresql://localhost:5432/{DB_NAME}",
        "schema": "lusha",
        "table": "contacts_data",
    }
