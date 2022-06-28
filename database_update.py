from genericpath import exists
from operator import index
import os
import sys
import shelve
import logging
from pathlib import Path
from decouple import config
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# -- INIT CONFIG --

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s -  %(levelname)s -  %(message)s"
)
logging.disable(logging.CRITICAL)

os.chdir(sys.path[0])
logging.debug(f"CWD is {Path.cwd()}")


# -- SCRIPT --

db_user = config("DB_USER")
db_password = config("DB_PASS")
db_host = config("DB_HOST")
db_name = config("DB_NAME")

# Create database in server if not exists
con = psycopg2.connect(
    dbname="postgres", user=db_user, host=db_host, password=db_password
)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = \'{db_name}\'")
exists = cur.fetchone()
if not exists:
    cur.execute(f"CREATE DATABASE {db_name}")
cur.close()
con.close

# Create tables in database
shelf_file = shelve.open("temp/df_processed")
df_processed_Dict = shelf_file["df_processed_Dict"]
shelf_file.close()

logging.debug(f"{db_user} : {db_password}")

engine = create_engine(f"postgresql://{db_user}:{db_password}@localhost:5432/alkemy_da")

try:
    for name, df in df_processed_Dict.items():
        df.to_sql(name, engine, index=False, if_exists="replace")
        print(f"{name} actualizada satisfactoriamente...")
except Exception as err:
    raise SystemExit("Usuario o Contraseña incorrectos \n")

print("Actualización de bases de datos completada.")
