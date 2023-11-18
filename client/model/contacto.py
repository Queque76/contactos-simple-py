"""Agenda de Contactos - Cliente - Contacto."""
# Predefined naming style: snake_case

# [qbdev] The Contacto class will store the information of the Contacto entity of the database.


class Contacto:
    """Class that represents a contact."""
    def __init__(self):
        self.__id = ""
        self.__nombre = ""
        self.__apellidos = ""
        self.__fecha_nacimiento = ""
        self.__lista_telefonos = ""
        self.__lista_direcciones = ""

    def get_id(self):
        """Method that returns the contact identifier in the database."""
        return self.__id

    def get_nombre(self):
        """Method that returns the contact's first name."""
        return self.__nombre

    def get_apellidos(self):
        """Method that returns the contact's last name."""
        return self.__apellidos

    def get_fecha_nacimiento(self):
        """Method that returns the date of birth of the contact."""
        return self.__fecha_nacimiento

    def get_lista_telefonos(self):
        """Method that returns the contact's phone numbers."""
        return self.__lista_telefonos

    def get_lista_direcciones(self):
        """Method that returns contact addresses."""
        return self.__lista_direcciones

    def set_nombre(self, nombre):
        """Method that establishes or modifies the contact's first name."""
        self.__nombre = nombre

    def set_apellidos(self, apellidos):
        """Method that establishes or modifies the contact's last name."""
        self.__apellidos = apellidos

    def set_fecha_nacimiento(self, fechanacimiento):
        """Method that establishes or modifies the date of birth of the contact."""
        self.__fecha_nacimiento = fechanacimiento

    def set_lista_telefonos(self, listatelefonos):
        """Method that establishes or modifies the contact's phone numbers."""
        self.__lista_telefonos = listatelefonos

    def set_lista_direcciones(self, listadirecciones):
        """Method that establishes or modifies contact addresses."""
        self.__lista_direcciones = listadirecciones
