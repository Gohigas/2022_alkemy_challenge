import datetime
import logging
import os
import shelve
import sys
from pathlib import Path

import requests


# -- FUNCTIONS --
def url_request(category, url):
    """
    Request from given url and calls file_save funtion.

    :input: Type of facility as string. Url as string.
    :output: None.
    """
    try:
        res = requests.get(url, allow_redirects=True)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    file_save(category, res)
    return


def file_save(category, res):
    """
    Create folder with current date info and category, and save requested file.

    :input: Type of facility as string. requested object as string.
    :output: None.
    """
    month_Names = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }

    today = datetime.datetime.now()

    folder_name = "-".join([str(today.year), month_Names[today.month]])
    file_name = "-".join(
        [category, str(today.day).zfill(2), str(today.month).zfill(2), str(today.year)]
    )
    file_path = Path.cwd() / "data" / category / folder_name

    # Create folder:
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    # Save file:
    with open(file_path / "".join([file_name, ".csv"]), "wb") as output_file:
        for chunk in res.iter_content(100000):
            output_file.write(chunk)

    files_path_Dict[category] = file_path / "".join([file_name, ".csv"])
    logging.debug(files_path_Dict[category])
    return


# -- URLs --
url_Dict = {
    "museos": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv",
    "cines": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
    "bibliotecas": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv",
}


# -- INIT CONFIG --
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s -  %(levelname)s -  %(message)s"
)
logging.disable(logging.CRITICAL)

os.chdir(sys.path[0])
logging.debug(f"CWD is {Path.cwd()}")

if not os.path.isdir(Path.cwd() / "data"):
    os.makedirs(Path.cwd() / "data")
if not os.path.isdir(Path.cwd() / "temp"):
    os.makedirs(Path.cwd() / "temp")


# -- SCRIPT --
shelf_file = shelve.open("temp/last_files")
files_path_Dict = {}

for k, v in url_Dict.items():
    url_request(k, v)
    print(f"Archivo fuente de {k} descargada satisfactoriamente...")

shelf_file["files_path_Dict"] = files_path_Dict
shelf_file.close()

print("Descarga de archivos fuente completada.")
