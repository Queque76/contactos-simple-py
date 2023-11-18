# Agenda de Contactos - Simple
_contactos-simple-py_  
_Basic contact book, Client-Server model, multithreaded, with sockets and SQL database for Windows command terminal made in Python._  
_Versión v1.0.0_

### RESUMEN

Implementación, en Python 3 para plataformas Windows, de una agenda de contactos básica (información personal, teléfonos y direcciones) almacenada en una base de datos SQL (SQLite), manejada por un servidor con comunicaciones mediante sockets y al cual pueden acceder clientes (multihilo) conociendo su dirección y puerto de comunicaciones. Tanto cliente como servidor se lanzarán y manejarán desde el terminal de comandos de Windows, ya que esta aplicación no tiene interfaz gráfica.  

### DETALLES DE IMPLEMENTACIÓN

El servidor se configura mediante un fichero especificado en el módulo `/config/config.py`, el cual indica la ruta (relativa respecto al directorio base del proyecto) a un fichero de configuración principal (_.ini_) y a un segundo fichero de configuración alternativo (_.json_). Estos ficheros de configuración indican, a su vez, la ruta (también relativa) a la base de datos (SQLite), la dirección IP del servidor (host o hostname) y el puerto en el que está escuchando. Estas rutas son relativas al directorio base del proyecto. Con esta información, se crea un socket TCP/IP.  

El servidor puede lanzarse con el argumento `-d` (debug) que provoca que el servidor muestre, en el terminal de comandos, los mensajes recibidos por parte de los clientes. Estos mensajes se basan en un mini-protocolo basado en cadenas de texto con delimitadores de los objetos y atributos ('*', '#', '|', '-', '&'). El cliente implementa funciones de verificación y validación de los datos de entrada (del usuario) mediante el uso de expresiones regulares y otras técnicas para evitar errores en el servidor a la hora de descodificar los mensajes recibidos.  

Todas las librerías y módulos utilizados pertenecen a [la biblioteca estándar de Python 3](https://docs.python.org/es/3/library/index.html), a excepción del módulo `keyboard`, el cual puede ser descargado mediante el comando:
```sh
./python -m pip install keyboard
```

Se ha intentado codificar,  en la medida de lo posible, conforme a la [guía de estilo PEP 8](https://peps.python.org/pep-0008/). Al mismo tiempo, se han respetado buenas prácticas de diseño, rendimiento y mantenibilidad en el código. Sin embargo, es evidente que existe margen de mejora. En este sentido, se ha buscado la modularidad en la organización y diseño del código (MVC) y la aplicación se ha fundamentado en el paradigma de la programación orientada a objetos. Asimismo, se ha aplicado programación defensiva mediante el manejo de excepciones y el uso de expresiones regulares para validar los datos de entrada. Queda pendiente la implementación de pruebas unitarias con el fin de garantizar, en la medida de lo posible, la calidad y la integridad del código.  

La estructura del proyecto sigue el patrón Modelo-Vista-Controlador (MVC) de manera aproximada, separando las responsabilidades del modelo, la vista y el controlador para mantener una estructura organizada y fácil de mantener.

## FORMA DE USO

### Requisitos:

* Python 3 para Windows
* Módulo `keyboard` (véase `requirements.txt`)

### Lanzamiento:
#### Servidor

1. Especificar en `/config/config.py` el nombre de los ficheros de configuración (`DEFAULT_CONFIG_FILENAME`, fichero principal y `ALTERNATIVE_CONFIG_FILENAME`, fichero de respaldo).  
\- Fichero `/config/config.py`:
![config.py](https://drive.google.com/uc?id=1HRyPW4rqJJCFlEhLIawPNM-ZvAdf1CfY)


2. Especificar en los ficheros de configuración anteriores la ruta relativa al fichero de la base de datos (`DB_PATH`), la dirección del servidor (`SERVER_HOST`) y el puerto de comunicaciones (`SERVER_PORT`).  
\- Fichero `/config/config.ini`:
![config.ini](https://drive.google.com/uc?id=16i9A5HvzBTxo40rrnnqFOzuBuemqV2lM)
\- Fichero `/config/config.json`:
![config.json](https://drive.google.com/uc?id=1SOixmgempdn8ez5q-If0I7g2jaLcFsup)


3. Lanzar el servidor, en un terminal de comandos y desde la ruta base del proyecto, con el comando:
```sh
./python -m server.main.server_main
```

_Nota_: El servidor puede lanzarse con parte de la depuración habilitada o deshabilitada. Para habilitarla, usar el argumento -d:
```sh
./python -m server.main.server_main -d
```
#### Clientes
1. Lanzar cada cliente en un terminal de comandos, desde la ruta base del proyecto, con el comando:
```sh
./python -m client.main.client_main
```

## 🔗 Links relacionados
- [La biblioteca estándar de Python - Python.org](https://docs.python.org/es/3/library/index.html)  
- [PEP 8 – Style Guide for Python Code - Python.org](https://peps.python.org/pep-0008/)  

## 🛠 Skills & Technologies
Algunas de las tecnologías, habilidades o paradigmas que se han intentado ejemplarizar en este proyecto son: python, programación orientada a objetos, estructura Modelo-Vista-Controlador, manejo de ficheros, manejo de bases de datos SQL, comunicación por sockets, multihilo, manejo de excepciones, uso de F-strings, uso de administradores de contexto, uso de expresiones regulares, modularidad y programación defensiva.

### ⏩ MEJORAS PROPUESTAS

Como mencionamos anteriormente, este proyecto tiene un gran potencial de mejora y expansión y, en este sentido, proponemos algunas de las mejoras y ampliaciones que podrían implementarse en futuras versiones, tales como:  

* Implementar la funcionalidad para agregar correos electrónicos a un usuario.
* Implementar un atributo `notas` a la clase `Contacto`.
* Permitir la selección del fichero de la base de datos.
* Habilitar al usuario para modificar la información de un contacto.
* Permitir al usuario exportar toda la agenda de contactos en formato JSON o texto plano (por ejemplo).
* Ofrecer la opción de seleccionar el idioma de la aplicación (español, inglés).
* Diseñar una interfaz gráfica para el cliente.
* Integrar una base de datos NoSQL (MongoDB) o RTDB (Firebase).
* Implementar pruebas unitarias.

## 🖐 Sobre mi
Soy un Ingeniero en Informática apasionado por la tecnología, pero de todo esto y de otros proyectos, ya hablaremos en otro momento... 😉
