#!/usr/bin/env python3

import json


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