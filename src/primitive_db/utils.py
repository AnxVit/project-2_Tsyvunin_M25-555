#!/usr/bin/env python3

import json

import src.primitive_db.constant as const
import src.primitive_db.decorators as dec


@dec.handle_db_errors
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
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data
    
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

@dec.handle_db_errors
def load_table_data(table_name):
    '''
    Load data table from file
    Parameters
    ----------
    table_name: string
        table name

    Returns
    -------
    list
        rowa table
    bool
        is exist table
    '''
    path = const.DATA_DIR + table_name + const.EXTENSION_TABLE
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def save_table_data(table_name, data):
    '''
    Save data table to file
    Parameters
    ----------
    table_name: string
        table name
    data: list[dict]
        rows table        
    Returns
    -------
    None
    '''
    path = const.DATA_DIR + table_name + const.EXTENSION_TABLE
    full_data = {table_name: data}
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(full_data, file)
            