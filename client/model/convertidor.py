"""Agenda de Contactos - Cliente - Convertidor."""
# Predefined naming style: snake_case

# [qbdev] This module converts Contacto type objects into a text string for sending through the socket.

from . import contacto
from . import telefono
from . import direccion


def contacto_a_cadena(contacto):
    """Function that converts Contacto type objects into a text string."""
    try:
        cadena_aux = ""
        # [qbdev] Inserts the personal data of the contact into the string.
        cadena_aux += "*"
        cadena_aux += contacto.get_nombre()
        cadena_aux += "|"
        cadena_aux += contacto.get_apellidos()
        cadena_aux += "|"
        cadena_aux += contacto.get_fecha_nacimiento()
        # [qbdev] Inserts the phone data of the contact into the string.
        cadena_aux += "#"
        lista_telefonos = contacto.get_lista_telefonos()
        if lista_telefonos is not None:
            for telefono_aux in lista_telefonos:
                cadena_aux += "-"
                cadena_aux += str(telefono_aux.get_numero_telefono())
                cadena_aux += "|"
                cadena_aux += str(telefono_aux.get_descripcion())
        # [qbdev] Inserts the address data of the contact into the string.
        cadena_aux += "#"
        lista_direcciones = contacto.get_lista_direcciones()
        if lista_direcciones is not None:
            for direccion_aux in lista_direcciones:
                cadena_aux += "-"
                cadena_aux += str(direccion_aux.get_calle())
                cadena_aux += "|"
                cadena_aux += str(direccion_aux.get_piso())
                cadena_aux += "|"
                cadena_aux += str(direccion_aux.get_ciudad())
                cadena_aux += "|"
                cadena_aux += str(direccion_aux.get_codigo_postal())
        return cadena_aux
    except Exception as e:
        print("ERROR. Excepción:", type(e).__name__, e.args)
        print("ERROR. No puede convertirse el objeto tipo Contacto a cadena.")
        return None
