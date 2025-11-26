#!/usr/bin/env python3

import src.primitive_db.constant as const


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