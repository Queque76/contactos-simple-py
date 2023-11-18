"""Agenda de Contactos - Servidor - Teléfono."""
# Predefined naming style: snake_case

# [qbdev] The Telefono class will store the information of the Telefono entity of the database.

class Telefono:
    """Class that represents a telephone number."""
    def __init__(self, idtelefono, numerotelefono, descripcion):
        """Initialize the Telefono object."""
        self.__id = idtelefono
        self.__numero_telefono = numerotelefono
        self.__descripcion = descripcion
    
    def get_id(self):
        """Method that returns the telephone number identifier in the database."""
        return self.__id

    def get_numero_telefono(self):
        """Method that returns the telephone number."""
        return self.__numero_telefono

    def get_descripcion(self):
        """Method that returns the description of the telephone number."""
        return self.__descripcion

    def set_numero_telefono(self, numerotelefono):
        """Method that establishes or modifies the telephone number."""
        self.__numero_telefono = numerotelefono

    def set_descripcion(self, descripcion):
        """Method that establishes or modifies the description of the telephone number."""
        self.__descripcion = descripcion
