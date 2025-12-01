#!/usr/bin/env python3

import src.primitive_db.constant as const


def parse_where_set(items):
    if len(items) == 0:
        return
    match items[0]:
        case "where":
            return {items[1]: parse_str_to_valid_type(items[3])}
        case "set":
            return {items[1]: 
                    parse_str_to_valid_type(items[3])}, parse_where_set(items[4:])

def parse_str_to_valid_type(value):
    if value in const.TRUE_VALUES:
        return True
    if value in const.FALSE_VALUES:
        return False
    try:
        int_val = int(value)
        return int_val
    except (ValueError, TypeError):
        return value 
    