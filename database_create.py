from operator import index
import os
import sys
import shelve
import pandas as pd
from sqlalchemy import create_engine
# import psycopg2
import time

os.chdir(sys.path[0])

shelf_file = shelve.open("temp/df_processed")
df_processed_Dict = shelf_file["df_processed_Dict"]
shelf_file.close()

# db_user = os.environ.get('DB_USER')
# db_password = os.environ.get('DB_PASS')

while True:
    db_user = input("Ingrese el usuario de su base de datos(predeterminado: 'postgres'):")
    if db_user == "":
        db_user = "postgres"
        
    db_password = input("Ingrese la contraseña de su base de datos(predeterminado: 'password'):")
    if db_password == "":
        db_password = 'password'
    
    time.sleep(0.25)
        
    engine = create_engine(f"postgresql://{db_user}:{db_password}@localhost:5432/alkemy_da")
    
    try:
        for name, df in df_processed_Dict.items():
            df.to_sql(name, engine, if_exists="replace", index=False)
    except Exception:
        print("Usuario o Contraseña incorrectos \n")
        time.sleep(0.5)
        continue

    break

print("Base de datos actualizada satisfactoriamente")
