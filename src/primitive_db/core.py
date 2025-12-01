#!/usr/bin/env python3

import os

import src.primitive_db.constant as const
import src.primitive_db.utils as u


def create_table(metadata, table_name, columns):
    '''
    Create table
    Parameters
    ----------
    metadata: dict
        info about existing tables
    table_name: string
        table name
    colums: list[str]
        table columns in format (name:type)

    Returns
    -------
    dict
        updating metadata
    '''
    if not isinstance(metadata, dict):
        raise TypeError("Неверный тип метаданных")
    
    if not isinstance(table_name, str):
        raise TypeError("Неверный тип имени таблицы")
    
    if not isinstance(columns, list | str):
        raise TypeError("Неверный тип столбца(ов)")
    
    if table_name in metadata:
        raise ValueError(f"Таблица {table_name} уже существует")
    
    columns_meta = [f"{const.ID_COLUMN}:{const.INT_TYPE}"]
    for column in columns:
        if ":" not in column:
            raise ValueError(
                f"Неверный формат колонки: '{column}'. Ожидается 'name:type'"
            )
        
        name, type = column.split(":", 1)

        name = name.strip()
        type = type.strip().lower()

        if not name:
            raise ValueError("Имя колонки не может быть пустым")

        if name == const.ID_COLUMN:
            continue
        
        if type not in const.SUPPORTED_TYPES:
            raise TypeError(f"Тип столбца {type} не подерживается")
        columns_meta.append(column)

    metadata[table_name] = columns_meta

    return metadata
        

def drop_table(metadata, table_name):
    '''
    Drop existing table
    Parameters
    ----------
    metadata: dict
        info about existing tables
    table_name: string
        table name

    Returns
    -------
    dict
        updating metadata
    '''
    if not isinstance(metadata, dict):
        raise TypeError("Неверный тип метаданных")
    
    if not isinstance(table_name, str):
        raise TypeError("Неверный тип имени таблицы")

    if table_name not in metadata:
        raise ValueError(f"Таблицы {table_name} не существует")
    
    del metadata[table_name]

    os.remove(const.DATA_DIR + table_name + const.EXTENSION_TABLE)

    return metadata

def list_tables(metadata):
    '''
    Create table
    Parameters
    ----------
    metadata: dict
        info about existing tables

    Returns
    -------
    list[str]
        tables name
    '''
    if not isinstance(metadata, dict):
        raise TypeError("Неверный тип метаданных")
    
    return list(metadata.keys())

def insert(metadata, table_name, values):
    if not isinstance(metadata, dict):
        raise TypeError("Неверный тип метаданных")
    
    if not isinstance(table_name, str):
        raise TypeError("Неверный тип имени таблицы")
    
    if not isinstance(values, list):
        raise TypeError("Неверный тип для строки значений")
    
    if table_name not in metadata:
        raise ValueError(f"Таблицы {table_name} не существует")
    
    if len(metadata[table_name]) - 1 != len(values):
        raise ValueError("Недостаточное кол-во значений")
    
    postprocess_data = {}
    data = u.load_table_data(table_name)
    id = len(data) + 1
    postprocess_data[const.ID_COLUMN] = id
    
    for column_number in range(1, len(metadata[table_name])):
        column = metadata[table_name][column_number]
        name, type = column.split(":", 1)

        value = values[column_number-1]

        if not isinstance(value, const.MAP_TYPES[type]):
            raise TypeError(f"Неправильный тип: {value}")
        
        postprocess_data[name] = value
    
    data.append(postprocess_data)
        
    u.save_table_data(table_name, data)
    return id

def select(table_data, where_clause=None):    
    if where_clause is None:
        return table_data
    
    if not isinstance(where_clause, dict):
        raise ValueError("Неверный тип условия")

    where_column, where_value = get_clause(where_clause)

    res = []
    for data in table_data:
        if data[where_column] == where_value:
            res.append(data)
    return res

def update(table_data, set_clause, where_clause):
    if not isinstance(where_clause, dict):
        raise ValueError("Неверный тип условия")
    if not isinstance(set_clause, dict):
        raise ValueError("Неверный тип изменения")
    
    where_column, where_value = get_clause(where_clause)
    set_column, set_value = get_clause(set_clause)

    res = []
    postprocess_data = []
    for data in table_data:
        if data[where_column] == where_value:
            data[set_column] = set_value
            res.append(data[const.ID_COLUMN])
        postprocess_data.append(data)

    return postprocess_data, res

def delete(table_data, where_clause):
    if not isinstance(where_clause, dict):
        raise ValueError("Неверный тип условия")
    
    where_column, where_value = get_clause(where_clause)

    res = []
    postprocess_data = []
    for data in table_data:
        if data[where_column] == where_value:
            res.append(data[const.ID_COLUMN])
        else:
            postprocess_data.append(data)
    return postprocess_data, res

def get_clause(clause):
    column = list(clause.keys())[0]
    value = clause[column]
    if column.upper() == const.ID_COLUMN:
        column = const.ID_COLUMN
    return column, value