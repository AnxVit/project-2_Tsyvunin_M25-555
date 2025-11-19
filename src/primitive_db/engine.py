#!/usr/bin/env python3

import prompt


def welcome():
    print("Первая попытка запустить проект!")
    print()
    print("***")
    show_help()

    return enter_command()

def enter_command():
    comand = prompt.string('Введите команду: ')
    print()
    return comand

def show_help():
    print("<command> exit - выйти из программы")
    print("<command> help - выйти из программы")