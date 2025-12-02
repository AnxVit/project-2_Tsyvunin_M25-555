DATABASE_METADATA = "db_meta.json"

COMMAND_CREATE = "create_table"
COMMAND_DROP = "drop_table"
COMMAND_LIST = "list_tables"
COMMAND_EXIT = "exit"
COMMAND_HELP = "help"

COMMAND_INSERT = "insert"
COMMAND_SELECT = "select"
COMMAND_UPDATE = "update"
COMMAND_DELETE = "delete"
COMMAND_INFO = "info"

SUPPORTED_TYPES = ["int", "str", "bool"]

ID_COLUMN = "ID"
INT_TYPE = "int"

DATA_DIR = "data/"
EXTENSION_TABLE = ".json"

MAP_TYPES = {
    'int': int,
    'str': str,
    'bool': bool
}

TRUE_VALUES = ["True", "true"]
FALSE_VALUES = ["False", "false"]

CACHE_TTL = 10.0