from operator import index
import os
import sys
import shelve
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

os.chdir(sys.path[0])

shelf_file = shelve.open('temp/df_processed')
df_processed_Dict = shelf_file['df_processed_Dict']
shelf_file.close()

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')

engine = create_engine(f'postgresql://{db_user}:{db_password}@localhost:5432/alkemy_da')

for name, df in df_processed_Dict.items():
    df.to_sql(name, engine, if_exists = 'replace', index = False)
