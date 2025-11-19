#!/usr/bin/env python3

import src.primitive_db.engine as e


def main():
    print("DB project is running!")
    command = e.welcome()
    while command != "exit":
        match command:
            case "help":
                e.show_help()
            case _:
                print("Неизвестная команда")
        command = e.enter_command()

if __name__ == "__main__":
    main()