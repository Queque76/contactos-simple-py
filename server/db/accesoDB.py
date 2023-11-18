"""Agenda de Contactos - Servidor - AccesoDB."""
# Predefined naming style: snake_case

# [qbdev] The data access module is responsible for performing all operations related to the database.

import sqlite3
import traceback
import sys

from ..model import contacto
from ..model import direccion
from ..model import telefono


# [qbdev] Path to the database.
DATABASE_PATH = ""

# [qbdev] Constants for the SQL sequences to create the tables.
CREATE_CONTACTO_TABLE = """CREATE TABLE "Contacto" (
                            "Id" INTEGER NOT NULL UNIQUE,
                            "Nombre" TEXT NOT NULL,
                            "Apellidos" TEXT NOT NULL,
                            "FechaNacimiento" TEXT,
                            PRIMARY KEY("Id" AUTOINCREMENT))"""

CREATE_DIRECCION_TABLE = """CREATE TABLE "Direccion" (
                            "Id" INTEGER NOT NULL UNIQUE,
                            "ContactoId" INTEGER NOT NULL,
                            "Calle"	TEXT NOT NULL,
                            "Piso" TEXT NOT NULL,
                            "Ciudad" TEXT NOT NULL,
                            "CodigoPostal" TEXT NOT NULL,
                            PRIMARY KEY("Id" AUTOINCREMENT))"""

CREATE_TELEFONO_TABLE = """CREATE TABLE "Telefono" (
                            "Id" INTEGER NOT NULL UNIQUE,
                            "ContactoId" INTEGER NOT NULL,
                            "NumeroTelefono" TEXT NOT NULL,
                            "Descripcion" TEXT NOT NULL,
                            PRIMARY KEY("Id"))"""
CREATE_CORREO_TABLE = """CREATE TABLE "Correo" (
                            "Id" INTEGER NOT NULL UNIQUE,
                            "ContactoId" INTEGER NOT NULL,
                            "CorreoElectronico" TEXT NOT NULL,
                            "Descripcion" TEXT NOT NULL,
                            PRIMARY KEY("Id"))"""


class BaseDatos:
    """Class to manage the contact database."""
    def __init__(self):
        self.__ruta = DATABASE_PATH

    def leer_contactos(self):
        """Method to read contacts from database."""
        try:
            with sqlite3.connect(self.__ruta) as database:
                cursor_contacto = database.cursor()
                cursor_contacto.execute("SELECT * FROM Contacto")

                contactos = []

                for registro in cursor_contacto:
                    contacto_aux = contacto.Contacto(registro[0], registro[1], registro[2], registro[3])
                    contacto_aux.set_lista_telefonos(self.__leer_telefonos(database, contacto_aux.get_id()))
                    contacto_aux.set_lista_direcciones(self.__leer_direcciones(database, contacto_aux.get_id()))
                    contactos.append(contacto_aux)
                # [qbdev] By using with we ensure the closure of the DB even with exceptions.
                # database.close()
            return contactos
        except OSError:
            print("ERROR. No se pueden leer los contactos.")
            return []
        except sqlite3.Error as e:
            print("SQLite error: %s" % (" ".join(e.args)))
            print("Exception class is:", e.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []

    def __leer_telefonos(self, database, idcontacto):
        """Method to read contact phone numbers from the database."""
        try:
            cursor_telefono = database.cursor()
            cursor_telefono.execute("SELECT Id, NumeroTelefono, Descripcion FROM Telefono WHERE ContactoId = " + str(idcontacto))

            telefonos = []

            for registro in cursor_telefono:
                telefonos.append(telefono.Telefono(registro[0], registro[1], registro[2]))

            cursor_telefono.close()

            return telefonos
        except OSError:
            print("ERROR. No se pueden leer los teléfonos.")
            return []
        except sqlite3.Error as e:
            print("SQLite error: %s" % (" ".join(e.args)))
            print("Exception class is:", e.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []

    def __leer_direcciones(self, database, idcontacto):
        """Method to read the contact address from the database."""
        try:
            cursor_direccion = database.cursor()
            cursor_direccion.execute("SELECT Id, Calle, Piso, Ciudad, CodigoPostal FROM Direccion WHERE ContactoId = " + str(idcontacto))

            direcciones = []

            for registro in cursor_direccion:
                direcciones.append(direccion.Direccion(registro[0], registro[1], registro[2], registro[3], registro[4]))

            cursor_direccion.close()

            return direcciones
        except OSError:
            print("ERROR. No se pueden leer los teléfonos.")
            return []
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is:", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []

    def leer_contactos_nombre(self, nombre_p):
        """Method to read contacts by name."""
        try:
            with sqlite3.connect(self.__ruta) as database:
                cursor_contacto = database.cursor()
                cursor_contacto.execute("SELECT * FROM Contacto WHERE nombre = '" + nombre_p + "'")

                contactos = []

                for registro in cursor_contacto:
                    contacto_aux = contacto.Contacto(registro[0], registro[1], registro[2], registro[3])
                    contacto_aux.set_lista_telefonos(self.__leer_telefonos(database, contacto_aux.get_id()))
                    contacto_aux.set_lista_direcciones(self.__leer_direcciones(database, contacto_aux.get_id()))
                    contactos.append(contacto_aux)
                # [qbdev] By using with we ensure the closure of the DB even with exceptions.
                # database.close()
            return contactos
        except OSError:
            print("ERROR. No se pueden leer contactos por nombre.")
            return []
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is:", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []

    def leer_contactos_telefono(self, telefono_p):
        """Method to read contacts by phone number."""
        try:
            with sqlite3.connect(self.__ruta) as database:
                cursor = database.cursor()
                cursor.execute("SELECT * FROM Telefono WHERE NumeroTelefono = '" + telefono_p + "'")

                contactos = []

                for registro in cursor:
                    cursor_contacto = database.cursor()
                    cursor_contacto.execute("SELECT * FROM Contacto WHERE Id = " + str(registro[1]))

                    for registro_contacto in cursor_contacto:
                        contacto_aux = contacto.Contacto(registro_contacto[0], registro_contacto[1], registro_contacto[2], registro_contacto[3])
                        contacto_aux.set_lista_telefonos(self.__leer_telefonos(database, contacto_aux.get_id()))
                        contacto_aux.set_lista_direcciones(self.__leer_direcciones(database, contacto_aux.get_id()))
                        contactos.append(contacto_aux)
                # [qbdev] By using with we ensure the closure of the DB even with exceptions.
                # database.close()
            return contactos
        except OSError:
            print("ERROR. No se pueden leer contactos por teléfono.")
            return []
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is:", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []

    def insertar_contacto(self, contacto_p):
        """Method to insert a contact into the database."""
        try:
            with sqlite3.connect(self.__ruta) as database:
                cursor = database.cursor()
                info_contacto = (contacto_p.get_nombre(), contacto_p.get_apellidos(), contacto_p.get_fecha_nacimiento())
                cursor.execute("INSERT INTO Contacto (Nombre, Apellidos, FechaNacimiento) VALUES (?,?,?)", info_contacto)

                contactoid = cursor.lastrowid

                for telefono_aux in contacto_p.get_lista_telefonos():
                    info_telefono = (contactoid, telefono_aux.get_numero_telefono(), telefono_aux.get_descripcion())
                    cursor.execute("INSERT INTO Telefono (ContactoId, NumeroTelefono, Descripcion) VALUES (?,?,?)", info_telefono)

                for direccion_aux in contacto_p.get_lista_direcciones():
                    info_direccion = (contactoid, direccion_aux.get_calle(), direccion_aux.get_piso(), direccion_aux.get_ciudad(), direccion_aux.get_codigo_postal())
                    cursor.execute("INSERT INTO Direccion (ContactoId, Calle, Piso, Ciudad, CodigoPostal) VALUES (?,?,?,?,?)", info_direccion)
                # [qbdev] By using with we ensure the closure of the DB even with exceptions.
                # database.commit()
            return True
        except OSError:
            print("ERROR. No se puede insertar el contacto.")
            return False
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is:", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []

    def borrar_contacto(self, idcontacto):
        """Method to delete a contact from the database."""
        try:
            database = sqlite3.connect(self.__ruta)
            cursor = database.cursor()

            cursor.execute("DELETE FROM Telefono WHERE ContactoId = " + str(idcontacto))
            cursor.execute("DELETE FROM Direccion WHERE ContactoId = " + str(idcontacto))
            cursor.execute("DELETE FROM Contacto WHERE Id = " + str(idcontacto))

            database.commit()
            return True
        except OSError:
            print("ERROR. No se puede borrar el contacto.")
            return False
        except sqlite3.Error as er:
            print("SQLite error: %s" % (" ".join(er.args)))
            print("Exception class is:", er.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            return []


def init_database(databasepath):
    """Function that initializes the database."""
    print("[SERVER] [INFO] Inicializando la base de datos...")
    global DATABASE_PATH
    DATABASE_PATH = databasepath
    database = sqlite3.connect(DATABASE_PATH)

    try:
        database.execute(CREATE_CONTACTO_TABLE)
        print("[SERVER] [INFO] Se creó la tabla 'Contacto'.")
    except sqlite3.OperationalError:
        print("[SERVER] [INFO] La tabla 'Contacto' ya existe.")

    try:
        database.execute(CREATE_DIRECCION_TABLE)
        print("[SERVER] [INFO] Se creó la tabla 'Direccion'.")
    except sqlite3.OperationalError:
        print("[SERVER] [INFO] La tabla 'Direccion' ya existe.")

    try:
        database.execute(CREATE_TELEFONO_TABLE)
        print("[SERVER] [INFO] Se creó la tabla 'Telefono'.")
    except sqlite3.OperationalError:
        print("[SERVER] [INFO] La tabla 'Telefono' ya existe.")

    try:
        database.execute(CREATE_CORREO_TABLE)
        print("[SERVER] [INFO] Se creó la tabla 'Correo'.")
    except sqlite3.OperationalError:
        print("[SERVER] [INFO] La tabla 'Correo' ya existe.")

    print("[SERVER] [INFO] Base de datos inicializada.")

    database.close()

    return database
