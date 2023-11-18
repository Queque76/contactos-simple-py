"""Agenda de Contactos - Cliente."""
# Predefined naming style: snake_case

# [qbdev] Opens a socket for the client's connection to the server and sends and receives
#         information, controlling the flow of the program.

import os
import json
import configparser
import sys

from ..view import visualizacion
from ..view.visualizacion import TipoEntrada
from . import cliente
from ..config.config import *


DATA_RECV_AT_ONCE = 4096


def get_file_extension(filename):
    """Function to get the file extension."""
    return filename.split('.')[-1].lower()


def load_config_from_file(filename):
    """Function that loads client configuration from .ini or .json file."""
    extension = get_file_extension(filename)

    if os.path.isfile(filename):
        try:
            if extension == "ini":
                client_config = configparser.ConfigParser()
                client_config.read(filename)
            elif extension == "json":
                with open(filename, "r", encoding="utf-8") as file:
                    client_config = json.load(file)
            else:
                print(f"[CLIENT] [ERROR] El fichero '{filename}' no es compatible para configurar el cliente.")
                return None, None
            server_host = client_config['DEFAULT']['SERVER_HOST']
            server_port = int(client_config['DEFAULT']['SERVER_PORT'])
        except (configparser.Error, json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[CLIENT] [ERROR] Problema con el fichero de configuración '{filename}'.")
            print(f"[CLIENT] [ERROR] Excepción: {e}.")
            return None, None
        else:
            if not server_host or not isinstance(server_host, str):
                print("[CLIENT] [WARNING] Problema con el host del servidor.")
                return None, None
            elif not server_port or not isinstance(server_port, int):
                print("[CLIENT] [WARNING] Problema con el puerto del servidor.")
                return None, None
            else:
                print("[CLIENT] [INFO] Información de configuración correcta.")
                return server_host, server_port
    else:
        print(f"[CLIENT] [ERROR] No se encuentra el fichero '{filename}'.")
        return None, None


def main():
    """Client main function."""

    # [qbdev] We load the configuration from a .ini or .json file.
    print("[CLIENT] [INFO] Cargando configuración...")

    server_host, server_port = load_config_from_file(DEFAULT_CONFIG_FILENAME)

    if server_host is None or server_port is None:
        print(f"[CLIENT] [WARNING] Buscando fichero de configuración alternativo '{ALTERNATIVE_CONFIG_FILENAME}'")
        server_host, server_port = load_config_from_file(ALTERNATIVE_CONFIG_FILENAME)

    if server_host is None or server_port is None:
        print("[CLIENT] [WARNING] Problemas con los ficheros de configuración.")
        print("[CLIENT] [ERROR] Finalizando el programa...")
        sys.exit(EXIT_FAILURE)

    cliente_principal = cliente.Cliente(server_host, server_port)
    client_socket = cliente_principal.get_socket()

    while True:
        visualizacion.mostrar_menu()
        opcion_menu = visualizacion.obtener_opcion("Seleccione una opción: ", OPT_MAIN_MENU_OPTIONS)

        # [qbdev] Search Contacts (View).
        if opcion_menu == OPT_SEARCH_CONTACT:
            visualizacion.mostrar_menu_buscar()
            fin_buscar = False
            while not fin_buscar:
                opcion_buscar = visualizacion.obtener_opcion("Seleccione una opción: ", OPT_SEARCH_CONTACT_OPTIONS)
                if opcion_buscar == OPT_SEARCH_CONTACT_BY_NAME:
                    parametro = visualizacion.validar_datos_entrada(TipoEntrada.CADENA_TEXTO, "> Introduzca el nombre: ")
                    fin_buscar = True
                elif opcion_buscar == OPT_SEARCH_CONTACT_BY_PHONE:
                    parametro = visualizacion.validar_datos_entrada(TipoEntrada.TELEFONO, "> Introduzca el teléfono: ")
                    fin_buscar = True
                elif opcion_buscar == OPT_SEARCH_CONTACT_RETURN:
                    fin_buscar = True
            if opcion_buscar != OPT_SEARCH_CONTACT_RETURN:
                try:
                    mensaje = str(opcion_menu) + "&" + str(opcion_buscar) + "&" + parametro
                    client_socket.send(str.encode(mensaje))
                    recibido = client_socket.recv(DATA_RECV_AT_ONCE)
                    recibido = recibido.decode("utf-8")
                    visualizacion.mostrar_contactos(recibido)
                except Exception as e:
                    print("ERROR. Excepción:", type(e).__name__, e.args)
                    print("ERROR. En la búsqueda de contactos.")

        # [qbdev] Create contacts.
        elif opcion_menu == OPT_CREATE_NEW_CONTACT:
            try:
                nuevo_contacto = visualizacion.proceso_crear_contacto()
                client_socket.send(str.encode(str(opcion_menu) + "&" + nuevo_contacto))
                recibido = client_socket.recv(DATA_RECV_AT_ONCE)
                recibido = recibido.decode("utf-8")
                if recibido == CONTACT_INSERT_SUCCESS:
                    print("## Contacto insertado.")
                else:
                    print("ERROR. No se puede insertar el contacto.")
            except Exception as e:
                print("ERROR. Excepción:", type(e).__name__, e.args)
                print("ERROR. En la creación de contactos.")

        # [qbdev] Delete contacts.
        elif opcion_menu == OPT_DELETE_CONTACT:
            visualizacion.mostrar_menu_borrar()
            fin_borrar = False
            while not fin_borrar:
                opcion_borrar = visualizacion.obtener_opcion("Seleccione una opción: ", OPT_DELETE_CONTACT_OPTIONS)
                if opcion_borrar == OPT_DELETE_CONTACT_BY_NAME:
                    parametro = visualizacion.validar_datos_entrada(TipoEntrada.CADENA_TEXTO, "> Introduzca el nombre: ")
                    fin_borrar = True
                elif opcion_borrar == OPT_DELETE_CONTACT_BY_PHONE:
                    parametro = visualizacion.validar_datos_entrada(TipoEntrada.TELEFONO, "> Introduzca el teléfono: ")
                    fin_borrar = True
                elif opcion_borrar == OPT_DELETE_CONTACT_RETURN:
                    fin_borrar = True
            if opcion_borrar != OPT_DELETE_CONTACT_RETURN:
                try:
                    mensaje = str(opcion_menu) + "&" + str(opcion_borrar) + "&" + parametro
                    client_socket.send(str.encode(mensaje))
                    recibido = client_socket.recv(DATA_RECV_AT_ONCE)
                    recibido = recibido.decode("utf-8")
                    if recibido == CONTACT_DELETE_SUCCESS:
                        print("## Contacto borrado.")
                    elif recibido == CONTACT_DELETE_NOT_FOUND:
                        print("# El contacto no existe.")
                    else:
                        print("ERROR. No se puede borrar el contacto.")
                except Exception as e:
                    print("ERROR. Excepción:", type(e).__name__, e.args)
                    print("ERROR. En la eliminación de contactos.")

        # [qbdev] Show all contacts.
        elif opcion_menu == OPT_SHOW_ALL_CONTACTS:
            try:
                client_socket.send(str.encode(str(opcion_menu)))
                recibido = client_socket.recv(DATA_RECV_AT_ONCE)
                recibido = recibido.decode("utf-8")
                visualizacion.mostrar_contactos(recibido)
            except Exception as e:
                print("ERROR. Excepción:", type(e).__name__, e.args)
                print("ERROR. Mostrando todos los contactos.")

        # [qbdev] Exit the application.
        elif opcion_menu == OPT_EXIT_APPLICATION:
            client_socket.send(str.encode(str(opcion_menu)))
            print("[CLIENT] [INFO] > Cerrando cliente...")
            break

    cliente_principal.cerrar_socket()


# [qbdev] Execution is guaranteed only when you run the script directly.
if __name__ == '__main__': 
    main()
