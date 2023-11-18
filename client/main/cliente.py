"""Agenda de Contactos - Cliente - Cliente."""
# Predefined naming style: snake_case

# [qbdev] Cliente class implements a command terminal-based client that manages a contact book
#         against a server, with which it communicates through a socket (IP, TCP Stream).


import socket
import sys
import errno
from ..config.config import EXIT_FAILURE


class Cliente:
    """Class that implements a contact book client."""
    def __init__(self, host, port):
        """Initialize the client with the specified host and server port."""
        self.__server_host = host
        self.__server_port = port
        self.__socket = self.__crear_socket(host, port)

    def get__server_host(self):
        """Method that returns the server host."""
        return self.__server_host

    def get__server_port(self):
        """Method that returns the server port."""
        return self.__server_port

    def get_socket(self):
        """Method that returns the server's communications socket."""
        return self.__socket

    def set_server_host(self, host):
        """Method that establishes or modifies the server host."""
        self.__server_host = host

    def set_server_port(self, port):
        """Method that establishes or modifies the server port."""
        self.__server_port = port

    def set_socket(self, server_socket):
        """Method that establishes or modifies the server's communications socket."""
        self.__socket = server_socket

    def __crear_socket(self, server_host, server_port):
        """Method that creates a TCP/IP socket."""
        try:
            client_socket = socket.socket()
            client_socket.connect((server_host, server_port))
        except socket.error as e:
            if e.errno == errno.EACCES:
                print("[CLIENT] [ERROR] Permisos insuficientes para abrir el socket.")
            else:
                print("[CLIENT] [ERROR] Problema con el socket de comunicaciones.")
                print(f"[CLIENT] [ERROR] Exception: {e}.")
            sys.exit(EXIT_FAILURE)
        else:
            print("[CLIENT] [INFO] ¡Conectado al servidor!")
            print(f"[CLIENT] [INFO] > Servidor IP: {server_host} - Puerto: {server_port}")

        return client_socket

    def cerrar_socket(self):
        """Method that closes the client socket."""
        try:
            self.__socket.close()
        except socket.error as e:
            print(f"[CLIENT] [ERROR] Problema con el socket durante el close(): {e}")
