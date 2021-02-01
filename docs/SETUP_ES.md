# CÓMO CONFIGURAR EL AMBIENTE Y CORRER EL PROYECTO LOCALMENTE

## Backend

### Requisitos

- python 3.8
- python3-pip
- virtualenv

### Instalación

#### Linux

```
    # recuerda realizar una actualización general antes de instalar nuevos paquetes.
    sudo apt-get update

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

#### Mac

```
    [completar]
```

#### Windows

```
    [completar]
```

### Configuración

```
    # virtualenv encapsula las dependencias de python para que afecten sólo al proyecto ACADEMIA_BLOCKCHAIN.
    # Si es la primera vez que corres el proyecto, crea el entorno virtual para este proyecto.
    virtualenv acbc_env

    # Activa virtualenv.
    source acbc_env/bin/activate

    # Una vez virtualenv activo, instala las librerías listadas en requirements.txt
    pip install -r requirements.txt

    # Con las librerías instaladas está listo el entorno. Utilizamos el potente framework de desarrollo web Django.
    # Necesitas correr las migraciones de la base de datos.
    python manage.py migrate

    # Para eso no es necesario instalar postgresql (sqlite3 es suficiente), postgres se utiliza en el servidor.
    # La documentación de Django es extensa y muy bien detallada.
    
    # Puedes correr el servidor local
    python manage.py runserver
    
    # Puedes acceder al sitio en localhost:8000. 
    # Detienes el server local con Ctrl+C. 

    # Cuando finalizas tu desarrollo, desactiva virtualenv.
    deactivate
```

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
