#!/usr/bin/env python3

import shlex

import prompt
from prettytable import PrettyTable

import src.primitive_db.constant as const
import src.primitive_db.core as core
import src.primitive_db.decorators as dec
import src.primitive_db.parser as parse
import src.primitive_db.utils as u


def run():
    '''The main cycle of processing and running commands'''
    print_help()

    while True:
        metadata = u.load_metadata(const.DATABASE_METADATA)
        user_input = enter_command()
        args = shlex.split(user_input)
        command = args[0]

        match command:
            case const.COMMAND_CREATE:
                handle_create(args, metadata)
            case const.COMMAND_DROP:
                handle_drop(args, metadata)
            case const.COMMAND_LIST:      
                handle_list(args, metadata)
            case const.COMMAND_EXIT:
                return
            case const.COMMAND_HELP:
                print_help()
            case const.COMMAND_INSERT:
                handle_insert(args, metadata)
            case const.COMMAND_SELECT:
                handle_select(args, metadata)
            case const.COMMAND_UPDATE:
                handle_update(args, metadata)
            case const.COMMAND_DELETE:
                handle_delete(args, metadata)
            case const.COMMAND_INFO:
                handle_info(args, metadata)
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")

@dec.handle_db_errors
def handle_create(args, metadata):
    '''
    Create handler
    Validation, create meta info and table
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
    if len(args) < 2:
        raise ValueError(
            "Некорректное значение: <table_name>. Попробуйте снова."
        )
    metadata = core.create_table(metadata, args[1], args[2:])
    columns = ', '.join(metadata[args[1]])
    u.save_metadata(const.DATABASE_METADATA, metadata)
    print(f'Таблица {args[1]} успешно создана со столбцами: {columns}')

@dec.handle_db_errors
def handle_drop(args, metadata):
    '''
    Drop handler
    Validation, delete meta info and table
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
    if len(args) != 2:
        if len(args) == 1:
            raise ValueError(
                "Некорректное значение: <table_name>. Попробуйте снова."
            )
        else:
            raise ValueError(
                f"Некорректное значение: {args[2:]}. Попробуйте снова."
            )
    metadata = core.drop_table(metadata, args[1])
    u.save_metadata(const.DATABASE_METADATA, metadata)
    print(f"Таблица {args[1]} успешно удалена.")

@dec.handle_db_errors
def handle_list(args, metadata):
    '''
    List handler
    Validation, print name of tables
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
    if len(args) != 1:
        raise ValueError(
            f"Некорректное значение: {args[1:]}. Попробуйте снова."
        )
    tables = core.list_tables(metadata)
    print_tables(tables)

@dec.handle_db_errors
def handle_insert(args, metadata):
    '''
    Insert handler
    Validation, type mapping, insert row in table
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
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
    if args[2] not in metadata:
        raise KeyError("Такой таблицы не существует")
    
    table_name = args[2]
    values_str = ''.join(args[4:])
    values_list_str = values_str[1:-1].split(',')
    values = list(map(parse.parse_str_to_valid_type, values_list_str))
    id = core.insert(metadata, table_name, values)
    print(
        f"Запись с ID={id} успешно добавлена в таблицу \"{table_name}\"."
    )

@dec.handle_db_errors
def handle_select(args, metadata):
    '''
    Select handler
    Validation, parse where clause, print pretty table
    Cache using
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
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
    if args[2] not in metadata:
        raise KeyError("Такой таблицы не существует")
    
    where_clause = parse.parse_where_set(args[3:])
    table_name = args[2]
    table_data = u.load_table_data(table_name)
    res = core.select(table_data, where_clause)
    print_table_rows(metadata, table_name, res)

@dec.handle_db_errors
def handle_update(args, metadata):
    '''
    Update handler
    Validation, parse where/set clause, update value by condition
    Print ids of changed rows
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
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
    if args[1] not in metadata:
        raise KeyError("Такой таблицы не существует")
    
    set_clause, where_clause = parse.parse_where_set(args[2:])
    table_name = args[1]
    table_data = u.load_table_data(table_name)[table_name]
    table_data, ids = core.update(table_data, set_clause, where_clause)
    str_ids = ', '.join(list(map(str, ids)))
    u.save_table_data(table_name, table_data)
    print(
        f"Запись(и) с ID={str_ids} " \
        f"в таблице {table_name} успешно обновлена(ы)"
    )

@dec.handle_db_errors
def handle_delete(args, metadata):
    '''
    Update handler
    Validation, parse where clause, delete value by condition
    Print ids of deleted rows
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
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
    if args[2] not in metadata:
        raise KeyError("Такой таблицы не существует")
    
    where_clause = parse.parse_where_set(args[3:])
    table_name = args[2]
    table_data = u.load_table_data(table_name)[table_name]
    table_data, ids = core.delete(table_data, where_clause)
    str_ids = ', '.join(list(map(str, ids)))
    u.save_table_data(table_name, table_data)
    print(
        f"Запись(и) с ID={str_ids} " \
        f"успешно удалена(ы) из таблицы {table_name}."
    )

@dec.handle_db_errors
def handle_info(args, metadata):
    '''
    Info handler
    Validation, print table info
    Parameters
    ----------
    args: list[str]
        info about existing tables
    metadata: dict
        info about existing tables

    Returns
    -------
    None
    '''
    if len(args) != 2:
        raise ValueError(
            "Неправильный формат: info <table>"
        )
    if args[1] not in metadata:
        raise KeyError("Такой таблицы не существует")
    table_name = args[1]
    print_info(metadata, table_name)

def enter_command():
    '''
    Entering the user's command
    Parameters
    ----------
    None

    Returns
    -------
    str
        user's command
    '''
    command = prompt.string('Введите команду: ')
    print()
    return command

def print_tables(tables):
    '''
    Print name of tables
    Parameters
    ----------
    tables: list[str]
        tables name

    Returns
    -------
    None
    '''
    if not tables:
        print("Нет таблиц")
        return

    for i, table in enumerate(tables, 1):
        print(f"{i:2d}. {table}")
    print()

def print_table_rows(metadata, table_name, rows):
    '''
    Print rows of table
    Parameters
    ----------
    metadata: dict
        info about existing tables
    table_name: string
        table name
    rows: list[dict]
        rows of table
    Returns
    -------
    None
    '''
    table = PrettyTable()

    table.field_names = [column.split(":", 1)[0] for column in metadata[table_name]]
    for row in rows:
        table.add_row([x for x in row.values()])
    print(table)

def print_info(metadata, table_name):
    '''
    Print info about table
    Parameters
    ----------
    metadata: dict
        info about existing tables
    table_name: string
        table name
    Returns
    -------
    None
    '''
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(metadata[table_name])}")
    data = u.load_table_data(table_name)
    print(f"Количество записей: {len(data)}")


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print()

    print("***Операции с данными***")
    print("Функции:")
    print(("<command> insert into <имя_таблицы> values "
           "(<значение1>, <значение2>, ...) - создать запись."))
    print(("<command> select from <имя_таблицы> where <столбец>"
           " = <значение> - прочитать записи по условию."))
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(("<command> update <имя_таблицы> set <столбец1> = <новое_значение1>"
           " where <столбец_условия> = <значение_условия> - обновить запись."))
    print(("<command> delete from <имя_таблицы> where"
           " <столбец> = <значение> - удалить запись."))
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 