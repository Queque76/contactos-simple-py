"""Module with global variables of the client system."""

import os


# [qbdev] Application Exit.
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# [qbdev] Configuration Files.
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
DEFAULT_CONFIG_FILENAME = os.path.join(CONFIG_DIR, "config.ini")
ALTERNATIVE_CONFIG_FILENAME = os.path.join(CONFIG_DIR, "config.json")

# [qbdev] Interactive Commands & Menu Options.
CMD_SEARCH_CONTACT = "1"
CMD_SEARCH_CONTACT_BY_NAME = "1"
CMD_SEARCH_CONTACT_BY_PHONE = "2"
CMD_SEARCH_CONTACT_RETURN = "3"
CMD_CREATE_NEW_CONTACT = "2"
CMD_DELETE_CONTACT = "3"
CMD_DELETE_CONTACT_BY_NAME = "1"
CMD_DELETE_CONTACT_BY_PHONE = "2"
CMD_DELETE_CONTACT_RETURN = "3"
CMD_SHOW_ALL_CONTACTS = "4"
CMD_EXIT_APPLICATION = "5"

OPT_MAIN_MENU_OPTIONS = 5
OPT_SEARCH_CONTACT = 1
OPT_SEARCH_CONTACT_BY_NAME = 1
OPT_SEARCH_CONTACT_BY_PHONE = 2
OPT_SEARCH_CONTACT_RETURN = 3
OPT_SEARCH_CONTACT_OPTIONS = 3
OPT_CREATE_NEW_CONTACT = 2
OPT_DELETE_CONTACT = 3
OPT_DELETE_CONTACT_BY_NAME = 1
OPT_DELETE_CONTACT_BY_PHONE = 2
OPT_DELETE_CONTACT_RETURN = 3
OPT_DELETE_CONTACT_OPTIONS = 3
OPT_SHOW_ALL_CONTACTS = 4
OPT_EXIT_APPLICATION = 5

# [qbdev] Communications protocol message encoding.
CONTACT_INSERT_SUCCESS = "1"
CONTACT_INSERT_ERROR = "0"
CONTACT_INSERT_NOT_FOUND = "-1"
CONTACT_DELETE_SUCCESS = "1"
CONTACT_DELETE_ERROR = "0"
CONTACT_DELETE_NOT_FOUND = "-1"
CONTACT_SEARCH_EMPTY = "0"

# [qbdev] Main menu options.
# 1 : Buscar contacto
# 1.1 : Por nombre
# 1.2 : Por teléfono
# 1.3 : Volver
# 2 : Crear nuevo contacto
# 3 : Borrar contacto
# 3.1 : Por nombre
# 3.2 : Por teléfono
# 3.3 : Volver
# 4 : Mostrar todos los contactos
# 5 : Salir

# [qbdev] Some common exit codes and their meanings:
# Exit Code     Meaning
# 0             Success
# 1             General error or abnormal termination
# 2             Misuse of shell builtins
# 126           Command invoked cannot execute
# 127           Command not found
# 128           Invalid argument to exit
# 130           Script terminated by Control-C

# [qbdev] Some common status codes:
# Unexpected error.
# Specific error.
# Non-specific error.
# Different error.
# Other error.
# Successful operation.
# Operation not performed correctly.
# Unexpected error when entering information.
# Successful operation.
# Failed operation.
# Other results.
# Contact deleted.
# Non-existent contact.
# Error deleting contact.
# Contact inserted.
# Error inserting contact.
