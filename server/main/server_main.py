"""Agenda de Contactos - Servidor."""
# Predefined naming style: snake_case

# [qbdev] Open a socket for client connections by creating a thread for each connection.

import os
import json
import configparser
import sys
import threading
import sqlite3
import keyboard

from ..db import accesoDB
from ..communication import comunicaciones
from . import servidor
from ..config.config import (
    EXIT_SUCCESS,
    EXIT_FAILURE,
    DEFAULT_CONFIG_FILENAME,
    ALTERNATIVE_CONFIG_FILENAME
)


def get_file_extension(filename):
    """Function to get the file extension."""
    return filename.split('.')[-1].lower()


def load_config_from_file(filename):
    """Function that loads server configuration from .ini or .json file."""
    extension = get_file_extension(filename)

    if os.path.isfile(filename):
        try:
            if extension == "ini":
                server_config = configparser.ConfigParser()
                server_config.read(filename)
            elif extension == "json":
                with open(filename, "r", encoding="utf-8") as file:
                    server_config = json.load(file)
            else:
                print(f"[SERVER] [ERROR] El fichero '{filename}' no es compatible para configurar el servidor.")
                return None, None, None
            database_name = server_config['DEFAULT']['DB_PATH']
            server_host = server_config['DEFAULT']['SERVER_HOST']
            server_port = int(server_config['DEFAULT']['SERVER_PORT'])
        except (configparser.Error, json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[SERVER] [ERROR] Problema con el fichero de configuración '{filename}'.")
            print(f"[SERVER] [ERROR] Excepción: {e}.")
            return None, None, None
        else:
            if not database_name or not isinstance(database_name, str):
                print("[SERVER] [WARNING] Problema con el nombre de la base de datos.")
                return None, None, None
            elif not server_host or not isinstance(server_host, str):
                print("[SERVER] [WARNING] Problema con el host del servidor.")
                return None, None, None
            elif not server_port or not isinstance(server_port, int):
                print("[SERVER] [WARNING] Problema con el puerto del servidor.")
                return None, None, None
            else:
                print("[SERVER] [INFO] Información de configuración correcta.")
                return database_name, server_host, server_port
    else:
        print(f"[SERVER] [ERROR] No se encuentra el fichero '{filename}'.")
        return None, None, None


def handle_escape_key(server_instance):
    """Function to handle the ordered exit of the program when pressing the Esc (escape) key."""
    def signal_handler(e):
        if e.event_type == keyboard.KEY_DOWN and e.name == 'esc':
            print("[SERVER] [WARNING] > Programa interrumpido por el usuario. ¿Desea salir? (S/s): ", end="", flush=True)
            try:
                user_exit = input()
                if user_exit.lower() == "s":
                    print("[SERVER] [INFO] > Cerrando servidor...")
                    server_instance.cerrar_socket()
                    try:
                        server_instance.cerrar_database()
                    except sqlite3.ProgrammingError:
                        pass
                    sys.exit(EXIT_SUCCESS)
            except KeyboardInterrupt:
                pass

    #  [qbdev] Manage the ESC (escape) key, on Windows systems, using the keyboard library.
    if os.name == 'nt':
        keyboard.hook(signal_handler)


def main():
    """Server main function."""

    # [qbdev] Run it with the -d argument, the application displays commands received from clients.
    debug_on = len(sys.argv) == 2 and sys.argv[1] == "-d"
    print("[SERVER] [INFO] Depuración activada." if debug_on else
            "[SERVER] [INFO] Depuración desactivada.")

    # [qbdev] We load the configuration from a .ini or .json file.
    print("[SERVER] [INFO] Cargando configuración...")

    database_name, server_host, server_port = load_config_from_file(DEFAULT_CONFIG_FILENAME)

    if database_name is None or server_host is None or server_port is None:
        print(f"[SERVER] [WARNING] Buscando fichero de configuración alternativo '{ALTERNATIVE_CONFIG_FILENAME}'")
        database_name, server_host, server_port = load_config_from_file(ALTERNATIVE_CONFIG_FILENAME)

    if database_name is None or server_host is None or server_port is None:
        print("[SERVER] [WARNING] Problemas con los ficheros de configuración.")
        print("[SERVER] [ERROR] Finalizando el programa...")
        sys.exit(EXIT_FAILURE)

    server_database = accesoDB.init_database(database_name)

    servidor_principal = servidor.Servidor(server_host, server_port, server_database, debug_on)

    handle_escape_key(servidor_principal)

    while True:
        try:
            cliente, direccion = servidor_principal.accept_socket()
            print(f"[SERVER] [INFO] > Nuevo cliente conectado: {direccion[0]}:{direccion[1]}")
            hilo_cliente = threading.Thread(target=comunicaciones.hilo_cliente, args=(debug_on, cliente, f"{direccion[0]}:{direccion[1]}",))
            hilo_cliente.start()
        except ConnectionAbortedError:
            print("[SERVER] [ERROR] La conexión fue abortada durante el proceso de aceptación.")
            break
        except TypeError as e:
            print(f"[SERVER] [ERROR] TypeError: {e}")
            break
        except Exception as e:
            print(f"[SERVER] [ERROR] {e}")
            break
        except KeyboardInterrupt:
            handle_escape_key(servidor_principal)


# [qbdev] Execution is guaranteed only when you run the script directly.
if __name__ == "__main__":
    main()
