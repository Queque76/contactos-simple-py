"""Agenda de Contactos - Cliente - Visualización."""
# Predefined naming style: snake_case

# [qbdev] This module is responsible for displaying all messages on the screen.

import datetime
from datetime import date
from enum import Enum, unique
import math
import re
import sys

from ..config.config import EXIT_SUCCESS
from ..model import contacto
from ..model import telefono
from ..model import direccion
from ..model import convertidor


def mostrar_menu():
    """Function that displays the main menu of the application."""
    print("""
#######################################
#         AGENDA DE CONTACTOS         #          
#######################################
Menú principal
 1) Ver contacto
 2) Crear contacto nuevo
 3) Borrar contacto
 4) Mostrar todos los contactos
 5) Salir""")


def mostrar_menu_buscar():
    """Function that displays the contact search submenu."""
    print(""" Buscar contactos por:
 1) Por nombre
 2) Por número de teléfono
 3) Volver""")


def mostrar_menu_borrar():
    """Function that displays the contact deletion submenu."""
    print(""" Borrar contactos por:
 1) Por nombre
 2) Por número de teléfono
 3) Volver""")


def obtener_opcion(mensaje, opciones):
    """Function that requests and obtains the option chosen by the user."""
    aceptado = False
    while not aceptado:
        try:
            opcion = int(input(mensaje))
        except ValueError:
            print(f"ERROR. Debe introducir una opción válida [1-{opciones}].")
        except TypeError:
            print(f"ERROR. Debe introducir una opción válida [1-{opciones}].")
        except EOFError:
            print("ERROR. Se finalizó la entrada.")
        except KeyboardInterrupt:
            user_exit = input("\n[CLIENT] [WARNING] > Programa interrumpido por el usuario. ¿Desea salir? (S/s): ")
            if user_exit.lower() == "s":
                print("[CLIENT] [INFO] > Cerrando cliente...")
                sys.exit(EXIT_SUCCESS)
        else:
            if opcion < 1 or opcion > opciones:
                print(f"ERROR. Tienes que introducir una opción válida [1-{opciones}].")
            else:
                aceptado = True
    return opcion


# [qbdev] Enumerated for input types.
@unique
class TipoEntrada(Enum):
    """Class as an enumerator of abstract data types for user input data."""
    CADENA_TEXTO = 1
    TELEFONO = 2
    EMAIL = 3
    FECHA_ISO8601 = 4
    FECHA_HORA_ISO8601 = 5


# [qbdev] Function to count the number of digits in a number (integer, positive).
def contar_digitos(numero):
    """Function that counts how many digits there are in a positive integer."""
    if isinstance(numero, int):
        if numero < 0:
            print("ERROR. Número negativo.")
            return 0
        elif numero != 0:
            return (int(math.log10(numero)) + 1)
        else:
            return 1
    else:
        print("ERROR. Es un número racional.")
        return 0


# [qbdev] Function to validate text strings.
#         We do not allow the characters: "*", "#", "|", "-", "&", """, "'", "\"
def validar_cadena(mensaje):
    """Function that validates a text string entered by the user."""
    dato_aceptado = False
    no_admitidos = ["*", "#", "|", "-", "&", "\"", "\'", "\\"]
    intentos = 0
    while not dato_aceptado:
        try:
            cadena = input(mensaje)
        except EOFError:
            print("ERROR. Se finalizó la entrada.")
        except KeyboardInterrupt:
            user_exit = input("\n[CLIENT] [WARNING] > Programa interrumpido por el usuario. ¿Desea salir? (S/s): ")
            if user_exit.lower() == "s":
                print("[CLIENT] [INFO] > Cerrando cliente...")
                sys.exit(EXIT_SUCCESS)
        except Exception as e:
            print("ERROR. Excepción:", type(e).__name__, e.args)
        else:
            if not cadena or len(cadena.replace(" ", "")) == 0:
                intentos = intentos + 1
                if intentos < 2:
                    print("Ha introducido una cadena vacía. Por favor, "\
                        "confirme cadena vacía o introduzca una cadena válida.")
                elif intentos == 2:
                    cadena = "(No disponible)"
                    break
            elif len(cadena) < 65:
                for char in no_admitidos:
                    if char in cadena:
                        print(f"ERROR. Carácter introducido no válido: {char}")
                        intentos = 0
                        break
                else:
                    dato_aceptado = True
            else:
                print("ERROR. Cadena demasiado larga (máx: 64).")
                intentos = 0
    return cadena


# [qbdev] Function to validate a valid phone number (9 digits).
# TO DO. It could also be implemented with a regular expression.
def validar_telefono(mensaje):
    """Function that validates a nine digits telephone number entered by the user."""
    dato_aceptado = False
    while not dato_aceptado:
        try:
            # TO DO. With spaces in between, it does not validate the format (for example, 666 123 456).
            telefono = int(input(mensaje))
        except ValueError:
            print("ERROR. Debe introducir un número de teléfono válido (9 dígitos).")
        except TypeError:
            print("ERROR. Debe introducir un número de teléfono válido (9 dígitos).")
        except EOFError:
            print("ERROR. Se finalizó la entrada.")
        except KeyboardInterrupt:
            user_exit = input("\n[CLIENT] [WARNING] > Programa interrumpido por el usuario. ¿Desea salir? (S/s): ")
            if user_exit.lower() == "s":
                print("[CLIENT] [INFO] > Cerrando cliente...")
                sys.exit(EXIT_SUCCESS)
        else:
            if telefono < 1 or telefono > 999999999:
                print("ERROR. Debe introducir un número de teléfono válido (9 dígitos).")
            elif contar_digitos(telefono) != 9:
                print("ERROR. Debe introducir un número de teléfono válido (9 dígitos).")
            else:
                dato_aceptado = True
    return telefono


# [qbdev] Function to validate a valid email address.
#         We do not allow the characters: "*", "#", "|", "-", "&", """, "'", "\"
def validar_email(mensaje):
    """Function that validates a email address entered by the user."""
    dato_aceptado = False
    while not dato_aceptado:
        try:
            correo = input(mensaje)
        except EOFError:
            print("ERROR. Se finalizó la entrada.")
        except KeyboardInterrupt:
            user_exit = input("\n[CLIENT] [WARNING] > Programa interrumpido por el usuario. ¿Desea salir? (S/s): ")
            if user_exit.lower() == "s":
                print("[CLIENT] [INFO] > Cerrando cliente...")
                sys.exit(EXIT_SUCCESS)
        except Exception as e:
            print("ERROR. Excepción:", type(e).__name__, e.args)
        else:
            if len(correo) < 65:
                patron_correo = r"\b[A-Za-z0-9._%+]+@[A-Za-z0-9.]+\.[A-Z|a-z]{2,}\b"
                if re.match(patron_correo, correo) is not None:
                    dato_aceptado = True
                else:
                    print("ERROR. Debe introducir un correo electrónico válido (user@domain.tld).")
            else:
                print("ERROR. Cadena demasiado larga (máx: 64).")
    return correo

def validar_fecha_ISO8601(mensaje):
    """Function that validates an ISO 8601 date entered by the user."""
    dato_aceptado = False
    while not dato_aceptado:
        try:
            fecha_user = input(mensaje)
        except EOFError:
            print("ERROR. Se finalizó la entrada.")
        except KeyboardInterrupt:
            user_exit = input("\n[CLIENT] [WARNING] > Programa interrumpido por el usuario. ¿Desea salir? (S/s): ")
            if user_exit.lower() == "s":
                print("[CLIENT] [INFO] > Cerrando cliente...")
                sys.exit(EXIT_SUCCESS)
        except Exception as e:
            print("ERROR. Excepción:", type(e).__name__, e.args)
        else:
            if len(fecha_user) < 11:
                patron_DD_MM_YYYY = r"\b([1-9]|0[1-9]|[12]\d|3[01])[-/]([1-9]|0[1-9]|1[0-2])[-/](19\d\d|20\d\d)\b"
                if re.match(patron_DD_MM_YYYY, fecha_user) is not None:
                    if "-" in fecha_user:
                        fecha_aux = fecha_user.split("-")
                    else:
                        fecha_aux = fecha_user.split("/")
                    try:
                        fecha_ISO = datetime.date(int(fecha_aux[2]), int(fecha_aux[1]), int(fecha_aux[0]))
                        fecha_string = fecha_ISO.strftime('%Y-%m-%d')
                    except ValueError:
                        print("ERROR. Fecha inválida. Compruebe días del mes (30/31) y/o años bisiestos.")
                    else:
                        dato_aceptado = True
                        return fecha_string
                else:
                    print("ERROR. Debe introducir una fecha válida (DD-MM-YYYY).")
            else:
                print("ERROR. Cadena demasiado larga (máx: 10).")
    return fecha_string


# [qbdev] Function to obtain valid input data according to the abstract data type.
def validar_datos_entrada(tipo, mensaje):
    """Function that requests and obtains the option chosen by the user."""
    if tipo == TipoEntrada.CADENA_TEXTO:
        return validar_cadena(mensaje)
    if tipo == TipoEntrada.TELEFONO:
        return validar_telefono(mensaje)
    if tipo == TipoEntrada.EMAIL:
        return validar_email(mensaje)
    if tipo == TipoEntrada.FECHA_ISO8601:
        return validar_fecha_ISO8601(mensaje)
    else:
        return f"ERROR. El tipo ({tipo}) todavía no está soportado."


def mostrar_contactos(contactos):
    """Function that displays information about contacts."""
    try:
        print("\n############## CONTACTOS ##############")

        # [qbdev] Obtaining different contacts and deleting the first element,
        #         as it would be empty when the string begins with '*'.
        cadena = contactos.split("*")
        del cadena[0:1]

        if len(cadena) == 0:
            print("#                                     #")

        for contacto_aux in cadena:
            print(" ----  Contacto  ----")
            # [qbdev] Contact data.
            datos_contacto = contacto_aux.split("#")[0].split("|")
            print(" Nombre:", datos_contacto[0])
            print(" Apellidos:", datos_contacto[1])
            try:
                fecha_nacimiento = date.fromisoformat(datos_contacto[2])
            except ValueError:
                print("ERROR. Fecha inválida. Compruebe días del mes (30/31) y/o años bisiestos.")
            else:
                print(" Fecha de nacimiento:", fecha_nacimiento.strftime('%d/%m/%Y'))

            # [qbdev] Obtaining phones and deleting the first element,
            #         as it would be empty when the string begins with '#'.
            datos_telefono = contacto_aux.split("#")[1].split("-")
            del datos_telefono[0:1]

            if len(datos_telefono) > 0:
                for telefono_aux in datos_telefono:
                    print(" Teléfono: ", telefono_aux.split("|")[0], " (", telefono_aux.split("|")[1],")", sep="")

            # [qbdev] Obtaining addresses and deleting the first element,
            #         as it would be empty when the string begins with '#'.
            datos_direcciones = contacto_aux.split("#")[2].split("-")
            del datos_direcciones[0:1]

            if len(datos_direcciones) > 0:
                for direccion_aux in datos_direcciones:
                    print(" Dirección: ", direccion_aux.split("|")[0], ", ", direccion_aux.split("|")[1], ", ", direccion_aux.split("|")[2], ", ", direccion_aux.split("|")[3], sep="")
        print("#######################################")
    except Exception as e:
        print("ERROR. Excepción:", type(e).__name__, e.args)
        print("ERROR. No se pueden mostrar los contactos.")


def proceso_crear_contacto():
    """Function that is responsible for requesting all the information necessary to create a contact."""
    try:
        print("############ NUEVO CONTACTO ############")

        nuevo_contacto = contacto.Contacto()
        nuevo_contacto.set_nombre(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce el nombre del contacto: "))
        nuevo_contacto.set_apellidos(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce los apellidos del contacto: "))
        nuevo_contacto.set_fecha_nacimiento(validar_datos_entrada(TipoEntrada.FECHA_ISO8601, " > Introduce la fecha de nacimiento del contacto: "))

        telefonos = []
        fin_telefono = ""
        while fin_telefono not in ("No", "no", "NO"):
            fin_telefono = validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > ¿Quieres añadir un teléfono? Si / No: ")
            if fin_telefono.lower() == "si":
                nuevo_telefono = telefono.Telefono()
                nuevo_telefono.set_numero_telefono(validar_datos_entrada(TipoEntrada.TELEFONO, " > Introduce el teléfono del contacto: "))
                nuevo_telefono.set_descripcion(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce la descripción de este teléfono: "))

                telefonos.append(nuevo_telefono)
        nuevo_contacto.set_lista_telefonos(telefonos)

        direcciones = []
        fin_direcciones = ""
        while fin_direcciones not in ("No", "no", "NO"):
            fin_direcciones = validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > ¿Quieres añadir una dirección? Si / No: ")
            if fin_direcciones.lower() == "si":
                nueva_direccion = direccion.Direccion()
                nueva_direccion.set_calle(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce la calle de la dirección del contacto: "))
                nueva_direccion.set_piso(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce el piso de la dirección del contacto: "))
                nueva_direccion.set_ciudad(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce la ciudad de la dirección del contacto: "))
                nueva_direccion.set_codigo_postal(validar_datos_entrada(TipoEntrada.CADENA_TEXTO, " > Introduce el código postal de la dirección del contacto: "))

                direcciones.append(nueva_direccion)
        nuevo_contacto.set_lista_direcciones(direcciones)
        
        return convertidor.contacto_a_cadena(nuevo_contacto)
    except Exception as e:
        print("ERROR. Excepción:", type(e).__name__, e.args)
        print("ERROR. No ha podido crearse el contacto.")
        return None
