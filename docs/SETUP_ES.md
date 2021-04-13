# CÓMO CONFIGURAR EL AMBIENTE Y CORRER EL PROYECTO LOCALMENTE

## Backend

### Requisitos

- python 3.8
- python3-pip
- virtualenv o docker 

### Instalación de requisitos

#### Linux

    - recuerda realizar una actualización general antes de instalar nuevos paquetes.
    sudo apt-get update

##### Instalación con virtualenv
```
    # instalar python3
    sudo apt-get install python3
    # puedes confirmar la instalación con el comando: python3 --version

    # instalar pip3
    sudo apt-get install python3-pip
    # puedes confirmar la instalación con el comando: pip3 --version

    # instalar virtualenv
    sudo pip3 install virtualenv
    # puedes confirmar la instalación con el comando: virtualenv --version
``` 
##### Instalación con Docker (recomendada)
``` 
    # instalar python3
    sudo apt-get install python3
    # puedes confirmar la instalación con el comando: python3 --version

    # instalar pip3
    sudo apt-get install python3-pip
    # puedes confirmar la instalación con el comando: pip3 --version

    # installar docker (https://docs.docker.com/engine/install/ubuntu/)
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    # puedes confirmar la instalación con el comando: docker --version
    # o puedes verificar la correcta instalación corriendo la imagen `hello world`:
    sudo docker run hello-world

    # installar el complemento [docker-compose] (https://docs.docker.com/compose/install/)
``` 

#### Mac

```
    [completar]
```

#### Windows

##### Instalación con virtualenv
```
    # instalar python 3.8 (https://www.python.org/downloads/release/python-389/)
    # puedes confirmar la instalación con el comando: python3 --version

    # pip3 viene instalado junto a python
    # puedes confirmar la instalación con el comando: pip --version
    # actualiza pip con el comando: 
    py -m pip install -U pip

    ## instalar virtualenv
    pip install virtualenv
    #puedes confirmar la instalación con el comando: virtualenv --version
```
##### Instalación con Docker (recomendada)

    0. Instalar Windows Subsystem for Linux [wsl] (https://docs.microsoft.com/en-us/windows/wsl/install-win10).
    
    1. Installar Ubuntu LST desde Microsoft Store (https://www.microsoft.com/es-ar/p/ubuntu-2004-lts/9n6svws3rx71?rtc=1&activetab=pivot:overviewtab). 

    2. Installar Docker Desktop (https://docs.docker.com/docker-for-windows/install/)

    3. Desde la terminal de ubuntu.
    ```
    # recuerda realizar una actualización general antes de instalar nuevos paquetes.
    sudo apt-get update

    # instalar python3
    sudo apt-get install python3
    # puedes confirmar la instalación con el comando: python3 --version

    # instalar pip3
    sudo apt-get install python3-pip
    # puedes confirmar la instalación con el comando: pip3 --version
    ```

### Instalación del proyecto

#### Instalación Manual (con Virtualenv)

Virtualenv encapsula las dependencias de python para que afecten sólo al proyecto ACADEMIA_BLOCKCHAIN.
Si es la primera vez que corres el proyecto, crea el entorno virtual para este proyecto.
virtualenv acbc_env

    0. Una ves instalado virtualenv, activar el entorno virtual.
        - Linux y MacOs: `acbc_env/source bin/activate`
        - Windows: `acbc_env\Scripts\activate.bat`
    
    1. Clonar el repositorio.

    2. Entra en el directorio del proyecto.
    `cd academia_blockchain`

    3. Crea un archivo .env para configurar las variales de ambiente.

    4. Instala las librerías listadas en requirements.txt
    pip install -r requirements.txt

    5. Aplica las migraciones de la base de datos. 
    python manage.py migrate

    6. Cargar fixture de la base de datos. Así populas el sitio con objetos de prueba.
    python manage.py loaddata db_fixture.json

    7. Crea un super usuario de Django.
    python manage.py createsuperuser

##### Configuración del entorno

```
    # Con las librerías instaladas y el .evn configurado, está listo el entorno. Utilizamos el potente framework de desarrollo web Django.
    # Necesitas correr las migraciones de la base de datos. Para eso no es necesario instalar postgresql (sqlite3 es suficiente), postgres se utiliza en el servidor.
    # La documentación de Django es extensa y muy bien detallada.
    
    # Puedes correr el servidor local
    python manage.py runserver
    
    # Puedes acceder al sitio en localhost:8000. 
    # Detienes el server local con Ctrl+C. 

    # Cuando finalizas tu desarrollo, desactiva virtualenv.
    deactivate
```

#### Instalación con docker (Recomendada)

    1. Entrar en el directorio del proyecto.
    `cd academia_blockchain`

    2. Crear un archivo .env para configurar las variales de ambiente.

    3. Construir la imagen.
    `docker-compose build`

    4. Ejecutar la aplicación.
    `docker-compose up -d`

    5. Aplicar migraciones.
    `docker-compose run --rm backend python3 manage.py migrate`

    6. Cargar fixture de la base de datos. Así populas el sitio con objetos de prueba.
    `docker-compose run --rm backend python3 manage.py loaddata db_fixture.json`

    7. Crear un super usuario de Django.
    `docker-compose run --rm backend python3 manage.py createsuperuser`

    8. Acceder al sitio en localhost:8000 y entrar con las credenciales de superusuario creadas en el paso anterior.

#### Errores comunes

- Error: pg_config executable not found when installing psycopg2

    **Respuesta**: https://stackoverflow.com/questions/11618898/pg-config-executable-not-found

        `pg_config` está en `postgresql-devel` (`libpq-dev` para Debian/Ubuntu, `libpq-devel` para Centos/Cygwin/Babun). En Ubuntu:

        `sudo apt-get install libpq-dev python-dev`

- raise KeyError(key) from None. KeyError: 'ACADEMIA_BLOCKCHAIN_SKEY'

    **Respuesta**: debes setear la variable de ambiente ACADEMIA_BLOCKCHAIN_SKEY.

    ```
    # En la raiz del proyecto crear un archivo .env y completarlo con los nombres de las variables y sus valores. Por ejemplo:
    ACADEMIA_BLOCKCHAIN_SKEY="your-secret-key"

    # Cargar el archivo .env luego de levantar el virtualenv
    set -a; source ./.env; set +a

    # En la consola, puedes chequear que la variable fue cargada correctamente.
    echo $ACADEMIA_BLOCKCHAIN_SKEY
    ```

## Frontend

Algunos desarrollos de frontend necesitan ser compilados con webpack, como por ejemplo el de `certificate_preview`. Webpack generará unos archivos bundleados y los ubicará en el directorio `static/assets/build`.

#### Requisitos

- `node` y `npm`

#### Instalación

```
    # ir al directorio client.
    cd client

    # instalar dependencias
    npm install
```

### Configuración

```
    # en desarrollo, utilizar el hot reload
    npm run start

    # al finalizar el desarrollo, buildear los archivos resultantes.
    npm run build
```
