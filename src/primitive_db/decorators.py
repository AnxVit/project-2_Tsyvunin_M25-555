import time
from functools import wraps

import prompt

import src.primitive_db.constant as const


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError | TypeError as e:
            print(f"Ошибка валидации типа/переменной: {e}")
        except FileExistsError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            command = prompt.string(
                f"Вы уверены, что хотите выполнить \"{action_name}\"? [y/n]:"
            )
            if command == "y" or command == "yes":
                return func(*args, **kwargs)
            else:
                print(f"{action_name} не будет произведено")
                return None
        return wrapper
    return real_decorator

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start} секунд")
    return wrapper

def create_cacher():
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            value, exp = cache[key]
            if time.monotonic() - exp < const.CACHE_TTL:
                print("(*Использовался кэш*)")
                return value
            
            del cache[key]

        value = value_func()
        cache[key] = (value, time.monotonic())
        return value
    return cache_result
