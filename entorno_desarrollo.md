Amig@s programadores que quieran apoyar al proyecto, esta es la manera de correr el código localmente:

## Entorno de Desarrollo

### Instalación manual
Instalar python 3.8 en tu computador. Instalar pip. Luego instalar virtualenv (es un entorno virtual de python que ayuda a encapsular las librerías y dependencias 
para que no influyen a todo tu sistema, sino solamente al proyecto de academia blockchain). Una ves instalado virtualenv, activar el entorno virtual 
(`source bin/activate`). 

Con el entorno virtual activadoinstalar todas las librerías listadas en el archivo requirements.txt con el comando `pip install -r requirements.txt` . Aquí, puede
que algunos paquetes den problemas, específicamente el psycopg2 que es una conexión a postgres que necesita paquetes extra. Las soluciones son conocidas y fáciles
de encontrar en stackoverflow. 

Con las librerías instaladas esta listo el entorno. Utilizamos el potente framework de desarrollo web Django. Necesitas correr las migraciones de la base de datos - `python manage.py migrate` - Para eso no es necesario instalar postgresql (sqlite3 es suficiente), postgres se utiliza en el servidor. La documentación de Django es extensa y muy bien detallada. Puedes correr el servidor local con "python manage.py runserver" y acceder al sitio en localhost:8000. 

### Instalación con docker
1. Entrar en el directorio del proyecto.
`cd academia_blockchain`

2. Construir la imagen.
`docker-compose build`

3. Ejecutar la aplicación.
`docker-compose up -d`

4. Aplicar migraciones.
`docker-compose run --rm backend python3 manage.py migrate`

5. Cargar fixture de la base de datos. Así populas el sitio con objetos de prueba.
`docker-compose run --rm python manage.py loaddata db_fixture.json`

6. Crear un super usuario de Django.
`docker-compose run --rm backend python3 manage.py createsuperuser`

7. Acceder al sitio en localhost:8000 y entrar con las credenciales de superusuario creadas en el paso 4.


No es necesario conocer mucho de python para correr el proyecto. Si lo tuyo es el CSS o el JS, corres el servidor local y te dedicas a esa parte del código. 


## Por qué no ves Truffle + Solidity

En nuestro roadmap está el desarrollo de un contrato inteligente propio en la segunda fase del proyecto. Hay algunas decisiones de arquitectura que hay que tomar
antes de comenzar con esto. Los certificados se pueden guardar en la blockchain utilizando web3, no es necesario un entorno de desarrollo de contratos inteligentes
todavía. 


## Si encuentras errores

Por favor si encuentras errores toma un screenshot y compártelos, puedes hacerlo en un comentario aquí o, mejor, puedes abrir un issue aparte. Esto ayudará mucho 
al proceso de desarrollo colaborativo. 
