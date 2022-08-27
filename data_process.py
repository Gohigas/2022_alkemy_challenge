import logging
import os
import re
import shelve
import sys
from pathlib import Path

import pandas as pd


# -- FUNCTIONS --
def columns_process(category, df, original_columns_Dict):
    """
    Process columns for each of the dataframes.

    Rename columns of dataframes to match expected output,
    Delete not required columns from dataframes.
    :input: Type of facility as string,
    :input: Related Dataframe,
    :input: Expected and existing column names as a dictionary.
    :output: Processed Dataframe.
    """
    rename_Dict = {}
    for k, v in original_columns_Dict.items():
        if k in df.columns:
            pass
        else:
            try:
                reg_ex = re.compile(v, re.I)
                rename_Dict[list(filter(reg_ex.match, list(df)))[0]] = k
            except IndexError as err:
                print(f"Error: no matching for '{k}' in '{category}' dataframe")
                sys.exit(err)

    df_new = df.rename(columns=rename_Dict)
    df_new = df_new.drop(
        df_new.columns.difference(list(original_columns_Dict.keys())), axis=1
    )

    return df_new


# -- INIT CONFIG --
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s -  %(levelname)s -  %(message)s"
)
logging.disable(logging.CRITICAL)

os.chdir(sys.path[0])
logging.debug(f"CWD is {Path.cwd()}")


# -- SCRIPT --
shelf_file = shelve.open("temp/last_files")
files_path_Dict = shelf_file["files_path_Dict"]
shelf_file.close()

df_Dict = {}
df_processed_Dict = {}
for k, v in files_path_Dict.items():
    df_Dict[k] = pd.read_csv(
        v, encoding="utf-8", quotechar='"', na_values=["s/d", "nan"]
    )

# - Task 01 -
original_columns_Dict1 = {
    "cod_localidad": r"cod_loc",
    "id_provincia": r"idprovincia",
    "id_departamento": r"iddepartamento",
    "categoría": r"categoria|categoría",
    "provincia": r"provincia",
    "localidad": r"localidad",
    "nombre": r"nombre",
    "domicilio": r"domicilio|direccion|dirección",
    "código postal": r"cp",
    "número de teléfono": r"telefono|teléfono",
    "mail": r"mail",
    "web": r"web",
}

df_total_Dict = {}
for category, df in df_Dict.items():
    df_new = columns_process(category, df, original_columns_Dict1)
    df_total_Dict[category] = df_new

for df in df_total_Dict.values():
    assert list(next(iter(df_total_Dict.values()))) == list(df)

dframes = list(df_total_Dict.values())
df_total = pd.concat(dframes)

logging.debug(df_total.shape)

df_total["fecha de carga"] = pd.to_datetime("today").strftime("%d/%m/%y")

df_processed_Dict["tabla_total"] = df_total

print("Tabla N°1 creada satisfactoriamente...")

### Task 02:
original_columns_Dict2 = {
    "categoría": r"categoria|categoría",
    "provincia": r"provincia",
    "nombre": r"nombre",
    "fuente": r"fuente",
}

df_total_Dict = {}
for category, df in df_Dict.items():
    df_new = columns_process(category, df, original_columns_Dict2)
    df_total_Dict[category] = df_new

for df in df_total_Dict.values():
    assert list(next(iter(df_total_Dict.values()))) == list(df)

dframes = list(df_total_Dict.values())
df_temp = pd.concat(dframes)

logging.debug(df_temp.sample(n=3))
logging.debug(df_temp.shape)

df_categoria = df_temp.groupby("categoría", as_index=False).size()
df_categoria.rename(
    columns={"categoría": "referencia", "size": "registros"}, inplace=True
)

df_fuente = df_temp.groupby("fuente", as_index=False).size()
df_fuente.rename(columns={"fuente": "referencia", "size": "registros"}, inplace=True)

df_prov_categoria = df_temp.groupby(["provincia", "categoría"], as_index=False).size()
df_prov_categoria.insert(
    loc=0,
    column="referencia",
    value=df_prov_categoria[["provincia", "categoría"]].agg("_".join, axis=1),
)
df_prov_categoria.rename(columns={"size": "registros"}, inplace=True)
df_prov_categoria.drop(["provincia", "categoría"], axis=1, inplace=True)

df_registros = pd.concat([df_categoria, df_fuente, df_prov_categoria])

logging.debug(df_registros.shape)

df_registros["fecha de carga"] = pd.to_datetime("today").strftime("%d/%m/%y")

df_processed_Dict["tabla_registros"] = df_registros

print("Tabla N°2 creada satisfactoriamente...")

### Task 03:
original_columns_Dict3 = {
    "provincia": r"provincia",
    "cantidad de pantallas": r"pantallas",
    "cantidad de butacas": r"butacas",
    "cantidad de espacios INCAA": r"espacio_INCAA",
}

df_lugares_cines = columns_process("cines", df_Dict["cines"], original_columns_Dict3)


logging.debug(df_lugares_cines["cantidad de espacios INCAA"].unique())
df_lugares_cines["cantidad de espacios INCAA"] = df_lugares_cines[
    "cantidad de espacios INCAA"
].str.lower()
df_lugares_cines["cantidad de espacios INCAA"] = df_lugares_cines[
    "cantidad de espacios INCAA"
].map({"0": 0, "si": 1})
logging.debug(df_lugares_cines["cantidad de espacios INCAA"].unique())

df_lugares_cines["cantidad de espacios INCAA"] = pd.to_numeric(
    df_lugares_cines["cantidad de espacios INCAA"]
).astype("Int64")

df_lugares_cines = df_lugares_cines.groupby(["provincia"], as_index=False)[
    ["cantidad de pantallas", "cantidad de butacas", "cantidad de espacios INCAA"]
].sum()

logging.debug(df_lugares_cines.shape)

df_lugares_cines["fecha de carga"] = pd.to_datetime("today").strftime("%d/%m/%y")

df_processed_Dict["tabla_lugares_cines"] = df_lugares_cines

print("Tabla N°3 creada satisfactoriamente...")

### Save df_processed_Dict
shelf_file = shelve.open("temp/df_processed")
shelf_file["df_processed_Dict"] = df_processed_Dict
shelf_file.close()

print("Procesamiento de datos completado.")
