from db_operation import (create_database, view_database, drop_database, view_table_database,
                          view_structure, view_role, view_user, drop_table)
from create_tables import create_table

if __name__ == "__main__":
    while True:
        print("-" * 130, "\n",
              "create_DB - создать базу | "
              "drop_DB - удалить базу | "
              "drop_table - удалить таблицу | "
              "create_table - создать базу с таблицами \n "
              "view_table - посмотреть таблицы | "
              "view_DB - посмотреть базы | "
              "view_structure - посмотреть структуру таблицы \n"
              "view_role - роли пользователя | ",
              "view_user - все пользователи \n",
              "-" * 130
              )

        q = input("ваш выбор: ")
        if q == "quit":
            exit()

        if q == "create_DB":
            dtb = input("имя новой БД: ")
            create_database(dtb)
            input()
        if q == "create_table":
            create_table()
            input()

        if q == "view_DB":
            result = view_database()
            for row in result:
                print(*row)
            input()

        if q == "drop_DB":
            dtb = input("name database: ")
            result = drop_database(dtb)
            input()

        if q == "drop_table":
            dtb = input("name database: ")
            answer = view_table_database(dtb)
            print(f"Таблицы в {dtb}")
            for row in answer:
                print(*row)
            table = input("name table: ")
            result = drop_table(dtb, table)
            print(result)
            input()

        if q == "view_table":
            dtb = input("name database: ")
            result = view_table_database(dtb)
            if result is None:
                print(f"{dtb} нет в списке")
            else:
                for row in result:
                    print(*row)
                input()

        if q == "view_structure":
            dtb = input("name database: ")
            name_table = input("table name: ")
            result = view_structure(dtb, name_table)
            if result is None:
                print("таблицы не найдены или база отсутствует")
            else:
                print("_" * 20)
                print(f"database {dtb}, таблица {name_table}")
                for row in result:
                    print(row)
                print("_" * 20)
            input()

        if q == "view_role":
            dtb = input("ввести имя базы: ")
            result = view_role(dtb)
            if result is None:
                print("таблицы не найдены или база отсутствует")
            else:
                print("_" * 20)
                print("Пользователи и их права: ")
                for user in result:
                    print(f"Имя: {user[0]}")
                    print(f"Может войти: {user[1]}")
                    print(f"Суперпользователь: {user[2]}")
                    print(f"Наследует права: {user[3]}")
                    print(f"Может создавать роли: {user[4]}")
                    print(f"Может создавать базы данных: {user[5]}")
                    print(f"Обходит политики безопасности: {user[6]}")
                    print(f"Ограничение подключений: {user[7]}")
                    print()
            input()

        if q == "view_user":
            result = view_user()
            if result is None:
                print("нет доступа")
            else:
                print("*" * 30)
                for user in result:
                    print(user[0])
                print("*" * 30)
            input()
