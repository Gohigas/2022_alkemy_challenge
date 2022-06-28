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

Dirigirse al directorio en el cual se desea instalar el entorno virtual. Generalemente el directorio del proyecto o en '~\.virtualenvs' (con -virtualenvwrapper-) con el siguiente comando *(reemplazando ["C:\path\to\directory"] por la ruta al directorio deseado)*:

```bash
cd ["C:\path\to\directory"]
```

Dentro del directorio sonde se desea crear el entorno virtual, ejecutar el siguiente comando *(reemplazando [venv_name] por el nombre del entorno virtual)*:

```bash
virtualenv [venv_name]
```

### Instalación de las dependencias necesarias con pip

Activar el entorno virtual con el siguiente comando dentro del directorio en el que se ubica el entorno virtual:

```bash
.\venv_name\Scripts\activate.bat
```

Instalar las dependencias requeridas para el deploy del proyecto con pip:

```bash
pip install requests
pip install pandas
pip install SQLAlchemy
pip install python-decouple
```

### Configuración de la conexión a la base de datos



### Ejecución del proyecto
