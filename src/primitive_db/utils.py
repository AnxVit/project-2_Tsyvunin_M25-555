#!/usr/bin/env python3

import json

import src.primitive_db.constant as const


def load_metadata(filepath):
    '''
    Load tables info from file
    Parameters
    ----------
    filepath: str
        path of file

    Returns
    -------
    dict
        metadata of tables from file
    '''
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("База данных не найдена. Создается новая...")
        return {}

def save_metadata(filepath, data):
    '''
    Save metadata about tables in file
    Parameters
    ----------
    filepath: str
        path of file
    data: dict
        metadata about tables

    Returns
    -------
    None
    '''
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file)

def load_table_data(table_name):
    try:
        path = const.DATA_DIR + table_name + const.EXTENSION_TABLE
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data[table_name], True
    except FileNotFoundError:
        return [], False

def save_table_data(table_name, data):
    path = const.DATA_DIR + table_name + const.EXTENSION_TABLE
    full_data = {table_name: data}
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(full_data, file)

def validate_commands(args):
    command = args[0]
    match command:
        case const.COMMAND_CREATE:
            if len(args) < 2:
                raise ValueError(
                    "Некорректное значение: <table_name>. Попробуйте снова."
                )
        case const.COMMAND_DROP:
            if len(args) != 2:
                if len(args) == 1:
                    raise ValueError(
                        "Некорректное значение: <table_name>. Попробуйте снова."
                    )
                else:
                    raise ValueError(
                        f"Некорректное значение: {args[2:]}. Попробуйте снова."
                    )
        case const.COMMAND_LIST:
            if len(args) != 1:
                raise ValueError(
                    f"Некорректное значение: {args[1:]}. Попробуйте снова."
                )
        case const.COMMAND_INSERT:
            if len(args) > 3:
                if args[1] != "into" or args[3] != "values":
                    raise ValueError(
                        "Неправильный формат: insert into <table> values (...)"
                    )
            if len(args) < 5:
                raise ValueError(
                    "Неправильный формат: insert into <table> values (...)"
                )
            values = ''.join(args[4:])
            if values[0] != '(' or values[-1] != ")":
                 raise ValueError(
                    "Неправильный формат: insert into <table> values (...)"
                )
        case const.COMMAND_SELECT:
            if len(args) not in [3, 7]:
                raise ValueError(
                    "Неправильный формат: " \
                    "select from <table> (where <column> = <value>)"
                )
            if args[1] != "from":
                raise ValueError(
                    "Неправильный формат: " \
                    "select from <table> (where <column> = <value>)"
                )
            if len(args) > 3:
                if args[3] != "where" or args[5] != "=":
                    raise ValueError(
                        "Неправильный формат: " \
                        "select from <table> (where <column> = <value>)"
                    )
        case const.COMMAND_DELETE:
            if len(args) != 7:
                raise ValueError(
                    "Неправильный формат: " \
                    "delete from <table> where <column> = <value>"
                )
            if args[1] != "from" or args[3] != "where" or args[5] != "=":
                raise ValueError(
                    "Неправильный формат: " \
                    "delete from <table> where <column> = <value>"
                )
        case const.COMMAND_UPDATE:
            if len(args) != 10:
                raise ValueError(
                    "Неправильный формат: " \
                    "update <table> set <column> = <value> where <column> = <value>"
                )
            if args[2] != "set" or args[6] != "where":
                raise ValueError(
                    "Неправильный формат: " \
                    "update <table> set <column> = <value> where <column> = <value>"
                )
            if args[4] != "=" or args[8] != "=":
                raise ValueError(
                    "Неправильный формат: " \
                    "update <table> set <column> = <value> where <column> = <value>"
                )
        case const.COMMAND_INFO:
            if len(args) != 2:
                raise ValueError(
                    "Неправильный формат: info <table>"
                )