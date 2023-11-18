"""Agenda de Contactos - Servidor - Comunicaciones."""
# Predefined naming style: snake_case

# [qbdev] This module manages communications with each client and processes the operations requested by them.

import sqlite3

from ..db import accesoDB
from ..model import convertidor
from ..config.config import *

DATA_RECV_AT_ONCE = 1024


def hilo_cliente(debug, conexion, direccion):
    """Function that manages a connection with a client."""
    fin = False
    while not fin:
        try:
            recibido = conexion.recv(DATA_RECV_AT_ONCE)
            recibido = recibido.decode("utf-8")

            if debug:
                print(f"[SERVER] [DEBUG] > ({direccion}) Comando recibido: {recibido}")

            if recibido == CMD_EXIT_APPLICATION:
                fin = True

            mensaje = str(procesar_mensaje(recibido))
            conexion.send(str.encode(mensaje))
        except ConnectionAbortedError:
            print("[SERVER] [WARNING] > ConnectionAbortedError.")
            fin = True
        except Exception as e:
            print("ERROR. Hilo cliente.")
            print("ERROR. Excepción:", type(e).__name__, e.args)
            fin = True
    print(f"[SERVER] [INFO] > Cliente {direccion} desconectado")
    conexion.close()


def procesar_mensaje(mensaje):
    """Function that processes the message received from the client."""
    try:
        lista_mensaje = mensaje.split("&")
        # [qbdev] Search contact by name.
        if lista_mensaje[0] == CMD_SEARCH_CONTACT and lista_mensaje[1] == CMD_SEARCH_CONTACT_BY_NAME:
            return buscar_contacto_nombre(lista_mensaje[2])
        # [qbdev] Search contact by phone.
        if lista_mensaje[0] == CMD_SEARCH_CONTACT and lista_mensaje[1] == CMD_SEARCH_CONTACT_BY_PHONE:
            return buscar_contacto_telefono(lista_mensaje[2])
        # [qbdev] Create contact.
        if lista_mensaje[0] == CMD_CREATE_NEW_CONTACT:
            return crear_contacto(lista_mensaje[1])
        # [qbdev] Delete contact by name.
        if lista_mensaje[0] == CMD_DELETE_CONTACT and lista_mensaje[1] == CMD_DELETE_CONTACT_BY_NAME:
            return borrar_contacto_nombre(lista_mensaje[2])
        # [qbdev] Delete contact by phone number.
        if lista_mensaje[0] == CMD_DELETE_CONTACT and lista_mensaje[1] == CMD_DELETE_CONTACT_BY_PHONE:
            return borrar_contacto_telefono(lista_mensaje[2])
        # [qbdev] Search all contacts.
        if lista_mensaje[0] == CMD_SHOW_ALL_CONTACTS:
            return buscar_todos_los_contactos()
    except sqlite3.OperationalError:
        print("ERROR. OperationalError (mio).")
    except Exception as e:
        print("ERROR. Procesando el mensaje recibido.")
        print("ERROR. Excepción:", type(e).__name__, e.args)
        return ""


def crear_contacto(contactostring):
    """Function that creates a new contact."""
    contacto_aux = convertidor.cadena_a_contacto(contactostring.lstrip("*"))
    basedatos = accesoDB.BaseDatos()
    if basedatos.insertar_contacto(contacto_aux):
        return CONTACT_INSERT_SUCCESS
    else:
        return CONTACT_INSERT_ERROR


def buscar_todos_los_contactos():
    """Function that searches all contacts."""
    basedatos = accesoDB.BaseDatos()
    datos = basedatos.leer_contactos()
    if len(datos) > 0:
        return convertidor.contacto_a_cadena(datos)
    else:
        return CONTACT_SEARCH_EMPTY


def buscar_contacto_nombre(nombre):
    """Function that searches for a contact by name."""
    basedatos = accesoDB.BaseDatos()
    datos = basedatos.leer_contactos_nombre(nombre)
    if len(datos) > 0:
        return convertidor.contacto_a_cadena(datos)
    else:
        return CONTACT_SEARCH_EMPTY


def buscar_contacto_telefono(telefono):
    """Function that searches for a contact by their phone number."""
    basedatos = accesoDB.BaseDatos()
    datos = basedatos.leer_contactos_telefono(telefono)
    if len(datos) > 0:
        return convertidor.contacto_a_cadena(datos)
    else:
        return CONTACT_SEARCH_EMPTY


def borrar_contacto_nombre(nombre):
    """Function that deletes a contact by name."""
    basedatos = accesoDB.BaseDatos()
    datos = basedatos.leer_contactos_nombre(nombre)
    if len(datos) > 0:
        respuesta = CONTACT_DELETE_SUCCESS
    else:
        respuesta = CONTACT_DELETE_NOT_FOUND
    for contacto_aux in datos:
        if not basedatos.borrar_contacto(contacto_aux.get_id()):
            respuesta = CONTACT_DELETE_ERROR
    return respuesta


def borrar_contacto_telefono(telefono):
    """Function that deletes a contact by its phone number."""
    basedatos = accesoDB.BaseDatos()
    datos = basedatos.leer_contactos_telefono(telefono)
    if len(datos) > 0:
        respuesta = CONTACT_DELETE_SUCCESS
    else:
        respuesta = CONTACT_DELETE_NOT_FOUND
    for contacto_aux in datos:
        if not basedatos.borrar_contacto(contacto_aux.get_id()):
            respuesta = CONTACT_DELETE_ERROR
    return respuesta
