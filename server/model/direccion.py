"""Agenda de Contactos - Servidor - Dirección."""
# Predefined naming style: snake_case

# [qbdev] The Direccion class will store the information of the Direccion entity of the database.

class Direccion:
    """Class that represents the address of a person."""
    def __init__(self, iddireccion, calle, piso, ciudad, codigopostal):
        """Initialize the Direccion object."""
        self.__id = iddireccion
        self.__calle = calle
        self.__piso = piso
        self.__ciudad = ciudad
        self.__codigo_postal = codigopostal

    def get_id(self):
        """Method that returns the address identifier in the database."""
        return self.__id

    def get_calle(self):
        """Method that returns the street address."""
        return self.__calle

    def get_piso(self):
        """Method that returns the floor or street number of the address."""
        return self.__piso

    def get_ciudad(self):
        """Method that returns the city or state of the address."""
        return self.__ciudad

    def get_codigo_postal(self):
        """Method that returns the zip code of the address."""
        return self.__codigo_postal

    def set_calle(self, calle):
        """Method that establishes or modifies the street address."""
        self.__calle = calle

    def set_piso(self, piso):
        """Method that establishes or modifies the floor or street number of the address."""
        self.__piso = piso

    def set_ciudad(self, ciudad):
        """Method that establishes or modifies the city or state of the address."""
        self.__ciudad = ciudad

    def set_codigo_postal(self, codigopostal):
        """Method that establishes or modifies the zip code of the address."""
        self.__codigo_postal = codigopostal
