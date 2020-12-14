Amig@s programadores que quieran apoyar al proyecto, esta es la manera de correr el código localmente:

## Entorno de Desarrollo

Instalar python 3.8 en tu computador. Instalar pip. Luego instalar virtualenv (es un entorno virtual de python que ayuda a encapsular las librerías y dependencias 
para que no influyen a todo tu sistema, sino solamente al proyecto de academia blockchain). Una ves instalado virtualenv, activar el entorno virtual 
(source bin/activate). 

Con el entorno virtual activadoinstalar todas las librerías listadas en el archivo requirements.txt con el comando pip install -r requirements.txt . Aquí, puede
que algunos paquetes den problemas, específicamente el psycopg2 que es una conexión a postgres que necesita paquetes extra. Las soluciones son conocidas y fáciles
de encontrar en stackoverflow. 

Con las librerías instaladas esta listo el entorno. Utilizamos el potente framework de desarrollo web Django. La documentación de Django es extensa y muy bien
detallada. Puedes correr el servidor local con "python manage.py runserver" y acceder al sitio en localhost:8000. 

No es necesario conocer mucho de python para correr el proyecto. Si lo tuyo es el CSS o el JS, corres el servidor local y te dedicas a esa parte del código. 


## Por qué no ves Truffle + Solidity

En nuestro roadmap está el desarrollo de un contrato inteligente propio en la segunda fase del proyecto. Hay algunas decisiones de arquitectura que hay que tomar
antes de comenzar con esto. Los certificados se pueden guardar en la blockchain utilizando web3, no es necesario un entorno de desarrollo de contratos inteligentes
todavía. 


## Si encuentras errores

Por favor si encuentras errores toma un screenshot y compártelos, puedes hacerlo en un comentario aquí o, mejor, puedes abrir un issue aparte. Esto ayudará mucho 
al proceso de desarrollo colaborativo. 
