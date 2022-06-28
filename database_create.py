from operator import index
import os
import sys
import shelve
from sqlalchemy import create_engine
import time
import logging
from pathlib import Path
from decouple import config


# -- INIT CONFIG --

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s -  %(message)s")
# logging.disable(logging.CRITICAL)

os.chdir(sys.path[0])
logging.debug(f"CWD is {Path.cwd()}")


# -- SCRIPT --

shelf_file = shelve.open("temp/df_processed")
df_processed_Dict = shelf_file["df_processed_Dict"]
shelf_file.close()

db_user = config('DB_USER')   
db_password = config('DB_PASS')

logging.debug(f"{db_user} : {db_password}")
        
engine = create_engine(f"postgresql://{db_user}:{db_password}@localhost:5432/alkemy_da")
    
try:
    for name, df in df_processed_Dict.items():
        df.to_sql(name, engine, index=False, if_exists="replace")
        print(f'{name} actualizada satisfactoriamente...')
except Exception as err:
    print("Usuario o Contraseña incorrectos \n")
    time.sleep(0.5)
    raise SystemExit(err)

print("Actualización de bases de datos completada.")
