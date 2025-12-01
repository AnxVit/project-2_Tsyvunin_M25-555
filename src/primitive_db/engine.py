#!/usr/bin/env python3

import shlex

import prompt
from prettytable import PrettyTable

import src.primitive_db.constant as const
import src.primitive_db.core as core
import src.primitive_db.parser as parse
import src.primitive_db.utils as u


def run():
    '''The main cycle of processing and running commands'''
    print_help()

    while True:
        try:
            metadata = u.load_metadata(const.DATABASE_METADATA)
            user_input = enter_command()
            args = shlex.split(user_input)
        except Exception as e:
            print(f"Неожиданная ошибка при чтении/получении данных: {e}")
            return
        try:
            u.validate_commands(args)
            command = args[0]

            match command:
                case const.COMMAND_CREATE:
                    metadata = core.create_table(metadata, args[1], args[2:])
                    columns = ', '.join(metadata[args[1]])
                    print(f'Таблица {args[1]} успешно создана со столбцами: {columns}')
                case const.COMMAND_DROP:
                    metadata = core.drop_table(metadata, args[1])
                    print(f"Таблица {args[1]} успешно удалена.")
                case const.COMMAND_LIST:             
                    tables = core.list_tables(metadata)
                    print_tables(tables)
                case const.COMMAND_EXIT:
                    return
                case const.COMMAND_HELP:
                    print_help()
                case const.COMMAND_INSERT:
                    tab_name = args[2]
                    values_str = ''.join(args[4:])
                    values_list_str = values_str[1:-1].split(',')
                    values = list(map(parse.parse_str_to_valid_type, values_list_str))
                    id = core.insert(metadata, tab_name, values)
                    print(
                        f"Запись с ID={id} успешно добавлена в таблицу \"{tab_name}\"."
                    )
                case const.COMMAND_SELECT:
                    where_clause = parse.parse_where_set(args[3:])
                    table_name = args[2]
                    table_data, ok = u.load_table_data(table_name)
                    if not ok:
                        raise FileNotFoundError("Такой таблицы не существует")
                    res = core.select(table_data, where_clause)
                    print_table_rows(metadata, table_name, res)
                case const.COMMAND_UPDATE:
                    set_clause, where_clause = parse.parse_where_set(args[2:])
                    table_name = args[1]
                    table_data, ok = u.load_table_data(table_name)
                    if not ok:
                        raise FileNotFoundError("Такой таблицы не существует")
                    table_data, ids = core.update(table_data, set_clause, where_clause)
                    str_ids = ', '.join(list(map(str, ids)))
                    print(
                        f"Запись(и) с ID={str_ids} " \
                        f"в таблице {table_name} успешно обновлена(ы)"
                    )
                    u.save_table_data(table_name, table_data)
                case const.COMMAND_DELETE:
                    where_clause = parse.parse_where_set(args[3:])
                    table_name = args[2]
                    table_data, ok = u.load_table_data(table_name)
                    if not ok:
                        raise FileNotFoundError("Такой таблицы не существует")
                    table_data, ids = core.delete(table_data, where_clause)
                    str_ids = ', '.join(list(map(str, ids)))
                    print(
                        f"Запись(и) с ID={str_ids} " \
                        f"успешно удалена(ы) из таблицы {table_name}."
                    )
                    u.save_table_data(table_name, table_data)
                case const.COMMAND_INFO:
                    table_name = args[1]
                    print_info(metadata, table_name)
                case _:
                    raise ValueError(f"Функции {command} нет. Попробуйте снова.")

            u.save_metadata(const.DATABASE_METADATA, metadata)
        except (ValueError, TypeError) as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при обработке команд: {e}")

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
    table = PrettyTable()

    table.field_names = [column.split(":", 1)[0] for column in metadata[table_name]]
    for row in rows:
        table.add_row([x for x in row.values()])
    print(table)

def print_info(metadata, table_name):
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(metadata[table_name])}")
    size = len(u.load_table_data(table_name))
    print(f"Количество записей: {size}")


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