#!/usr/bin/env python3

import shlex

import prompt

import src.primitive_db.constant as const
import src.primitive_db.core as core
import src.primitive_db.utils as u


def run():
    print_help()

    while True:
        try:
            metadata = u.load_metadata(const.DATABASE_METADATA)
            user_input = enter_command()
            args = shlex.split(user_input)
        except Exception as e:
            print(f"Неожиданная ошибка при чтении/получении данных: {e}")
        try:
            command = args[0]

            match command:
                case const.COMMAND_CREATE:
                    if len(args) < 2:
                        raise ValueError(
                            "Некорректное значение: <table_name>. Попробуйте снова."
                        )
                    
                    metadata = core.create_table(metadata, args[1], args[2:])
                    columns = ', '.join(metadata[args[1]])
                    print(f'Таблица {args[1]} успешно создана со столбцами: {columns}')
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
                    
                    metadata = core.drop_table(metadata, args[1])
                    print(f"Таблица {args[1]} успешно удалена.")
                case const.COMMAND_LIST:
                    if len(args) != 1:
                        raise ValueError(
                            f"Некорректное значение: {args[1:]}. Попробуйте снова."
                        )
                                         
                    tables = core.list_tables(metadata)
                    print_tables(tables)
                case const.COMMAND_EXIT:
                    return
                case const.COMMAND_HELP:
                    print_help()
                case _:
                    raise ValueError(f"Функции {args[0]} нет. Попробуйте снова.")

            u.save_metadata(const.DATABASE_METADATA, metadata)
        except (ValueError, TypeError) as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при обработке команд: {e}")

def enter_command():
    comand = prompt.string('Введите команду: ')
    print()
    return comand

def print_tables(tables):
    if not tables:
        print("Нет таблиц")
        return

    for i, table in enumerate(tables, 1):
        print(f"{i:2d}. {table}")
    print()

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 