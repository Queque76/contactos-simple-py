"""Agenda de Contactos - Servidor - Servidor."""
# Predefined naming style: snake_case

# [qbdev] Servidor class implements a server with socket (IP, TCP Stream) communications and
#         a local SQLite database. Accepts requests from different clients using threads.


import socket
import sqlite3
import sys
import errno

from ..config.config import EXIT_SUCCESS, EXIT_FAILURE


class Servidor:
    """Class that implements a TCP/IP server with a local SQLite database."""
    def __init__(self, host, port, db, debug):
        """Initialize the server with the specified host, port, database, and debug settings."""
        self.__host = host
        self.__port = port
        self.__debug = debug
        self.__db = db
        self.__socket = self.__crear_socket(host, port)

    def get_host(self):
        """Method that returns the server host."""
        return self.__host

    def get_port(self):
        """Method that returns the server port."""
        return self.__port

    def get_debug(self):
        """Method that returns if server debug is enabled."""
        return self.__debug

    def get_db(self):
        """Method that returns the server database."""
        return self.__db

    def get_socket(self):
        """Method that returns the server's communications socket."""
        return self.__socket

    def set_host(self, host):
        """Method that establishes or modifies the server host."""
        self.__host = host

    def set_port(self, port):
        """Method that establishes or modifies the server port."""
        self.__port = port

    def set_debug(self, debug):
        """Method that establishes or modifies server debugging."""
        self.__debug = debug

    def set_db(self, db):
        """Method that establishes or modifies the server database."""
        self.__db = db

    def set_socket(self, server_socket):
        """Method that establishes or modifies the server's communications socket."""
        self.__socket = server_socket

    def __crear_socket(self, server_host, server_port):
        """Method that creates a TCP/IP socket."""
        try:
            server_socket = socket.socket()
            server_socket.bind((server_host, server_port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("[SERVER] [ERROR] La dirección ya está en uso.")
            elif e.errno == errno.EACCES:
                print("[SERVER] [ERROR] Permisos insuficientes para abrir el socket.")
            else:
                print("[SERVER] [ERROR] Problema con el socket de comunicaciones.")
                print(f"[SERVER] [ERROR] Exception: {e}.")
            sys.exit(EXIT_FAILURE)
        else:
            print("[SERVER] [INFO] ¡Servidor arrancado!")
            print(f"[SERVER] [INFO] > Servidor IP: {server_host} - Puerto: {server_port}")
            server_socket.listen()

        return server_socket

    def accept_socket(self):
        """Method that accepts an incoming connection request from a TCP client."""
        try:
            return self.__socket.accept()
        except OSError as e:
            if e.errno == 10038:
                print("[SERVER] [INFO] > Socket cerrado.")
                sys.exit(EXIT_SUCCESS)
            else:
                print(f"[SERVER] [ERROR] Problema con el socket durante el accept(): {e}")

    def cerrar_socket(self):
        """Method that closes the server socket."""
        try:
            self.__socket.close()
        except socket.error as e:
            print(f"[SERVER] [ERROR] Problema con el socket durante el close(): {e}")

    def cerrar_database(self):
        """Method that closes the server database."""
        try:
            self.__db.close()
        except sqlite3.ProgrammingError:
            print("[SERVER] [INFO] > Base de datos cerrada.")
        except sqlite3.Error:
            print("[SERVER] [ERROR] Problema con el cierre de la base de datos.")
