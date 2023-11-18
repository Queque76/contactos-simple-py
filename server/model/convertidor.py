"""Agenda de Contactos - Servidor - Convertidor."""
# Predefined naming style: snake_case

# [qbdev] This module converts Contacto type objects into a text string for sending through the socket and vice versa.

from . import contacto
from . import telefono
from . import direccion


def cadena_a_contacto(cadena):
    """Function that converts a text string into Contacto type objects."""
    try:
        # [qbdev] Obtaining contact data and creating the object with the values.
        datos_contacto = cadena.split("#")[0].split("|")
        contacto_aux = contacto.Contacto(0, datos_contacto[0], datos_contacto[1], datos_contacto[2])

        # [qbdev] Obtaining telephone numbers and deleting the first element since it would be
        #         empty at the beginning of the string with '#'.
        datos_telefono = cadena.split("#")[1].split("-")
        del datos_telefono[0:1]

        if len(datos_telefono) > 0:
            telefonos = []
            # [qbdev] Processing all telephone numbers and storing them in a list.
            for item in datos_telefono:
                telefono_aux = telefono.Telefono(0, item.split("|")[0], item.split("|")[1])
                telefonos.append(telefono_aux)
            # [qbdev] Add telephone numbers to the contact.
            contacto_aux.set_lista_telefonos(telefonos)
        
        # [qbdev] Obtaining addresses and deleting the first element since it would be
        #         empty at the beginning of the string with '#'.
        datos_direcciones = cadena.split("#")[2].split("-")
        del datos_direcciones[0:1]

        if len(datos_direcciones) > 0:
            direcciones = []
            # [qbdev] Processing all addresses and storing them in a list.
            for item in datos_direcciones:
                direccion_aux = direccion.Direccion(0, item.split("|")[0], item.split("|")[1], item.split("|")[2], item.split("|")[3])
                direcciones.append(direccion_aux)
            # [qbdev] Add addresses to the contact.
            contacto_aux.set_lista_direcciones(direcciones)
        
        return contacto_aux
    except Exception as e:
        print("ERROR. Excepción:", type(e).__name__, e.args)
        print("ERROR. No puede convertirse la cadena a objeto tipo Contacto.")
        return None


def contacto_a_cadena(contactos):
    """Function that converts Contacto type objects into a text string."""
    try:
        cadena_aux = ""
        # [qbdev] Each contact will be inserted into the string one by one.
        for contacto_aux in contactos:
            # [qbdev] Contact data.
            cadena_aux += "*"
            cadena_aux += contacto_aux.get_nombre()
            cadena_aux += "|"
            cadena_aux += contacto_aux.get_apellidos()
            cadena_aux += "|"
            cadena_aux += contacto_aux.get_fecha_nacimiento()
            # [qbdev] Contact's phone data.
            cadena_aux += "#"
            lista_telefonos = contacto_aux.get_lista_telefonos()
            if lista_telefonos is not None:
                for telefono_aux in lista_telefonos:
                    cadena_aux += "-"
                    cadena_aux += str(telefono_aux.get_numero_telefono())
                    cadena_aux += "|"
                    cadena_aux += str(telefono_aux.get_descripcion())
            # [qbdev] Address data for the contact.
            cadena_aux += "#"
            lista_direcciones = contacto_aux.get_lista_direcciones()
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
