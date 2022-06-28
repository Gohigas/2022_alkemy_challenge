# 2022_alkemy_DA

Proyecto creado en el contexto del 'Challenge Data Analytics - Python' de Alkemy.

## Objetivo

Crear un proyecto que consuma datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos.

## Utilización

Clonar o descargar el repositorio para generar una copia local en tu computadora.

### Creación de un entorno virtual

Abrir la consola de comandos. Instalar el paquete -virtualenv- con pip en caso de ser necesario con el siguiente comando:

```bash
pip install virtualenv
```

Dirigirse al directorio en el cual se desea instalar el entorno virtual (generalmente el directorio del proyecto o en '~\.virtualenvs') con el siguiente comando: <br>
*-"C:\path\to\directory"- : ruta al directorio deseado*

```bash
cd -"C:\path\to\directory"-
```

Dentro del directorio sonde se desea crear el entorno virtual, ejecutar el siguiente comando: <br>
*-venv_name- : nombre del entorno virtual*

```bash
virtualenv -venv_name-
```

### Instalación de las dependencias necesarias con pip

Activar el entorno virtual con el siguiente comando dentro del directorio en el que se ubica el entorno virtual:

```bash
.\venv_name\Scripts\activate.bat
```

Instalar las dependencias requeridas para el deploy del proyecto utilizando pip:

```bash
pip install requests
pip install pandas
pip install python-decouple
pip install SQLAlchemy
pip install psycopg2
```

Verificar la correcta instalación de las dependencias utilizando pip freeze:

```bash
pip freeze
```

### Configuración de la conexión a la base de datos

Para configurar las variables necesarias para la conexión a la base de datos se debe crear un archivo de texto ubicado en el directorio del proyecto llamado 'settings.ini'. Editar el archivo creado con un editor de texto incluyendo el siguiente contenido:<br>
*-your_db_user- : nombre de usuario del servidor (generalmente 'postgres')* <br>
*-your_db_pass- : contraseña del servidor* <br>
*-your_db_host- : nombre de usuario del servidor (generalmente 'localhost')* <br>
*-your_db_user- : nombre de la nueva base de datos que se desea crear*

```notepad
[settings]
DB_USER = -your_db_user-
DB_PASS = -your_db_password-
DB_HOST = -your_db_host-
DB_NAME = -name_of_new_database-
```

### Ejecución del proyecto

Ejecutar los scripts -.py-, dentro del directorio del proyecto y con el entorno virtual activado, con los siguiente comandos en orden:

```bash
python data_requests.py
python data_process.py
python database_update.py
```
