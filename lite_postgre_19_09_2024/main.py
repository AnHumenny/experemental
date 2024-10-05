from create_tables import create_table
import db_operation
import config

class Operation:
    def __init__(self):
        self.dtbs = db_operation.Pg(host=config.host, port=config.port, user=config.user,
                          password=config.password, database=config.database)

        q = input("ваш выбор: ")
        if q == "quit":
            exit()

        if q == "help":
            print("-" * 130, "\n",
                  "create_DB - создать базу |"
                  "create_user - создать пользователя | "  # доработать
                  "create_table - создать базу с таблицами \n "
                  "drop_DB - удалить базу | "
                  "drop_user - удалить пользователя | "  # доработать
                  "drop_table - удалить таблицу \n "
                  "view_table - посмотреть таблицы | "
                  "view_DB - посмотреть базы | "
                  "view_structure - посмотреть структуру таблицы \n "
                  "view_role - роли пользователя | ",
                  "view_user - все пользователи | \n",
                  "grant_DB - предоставить права на базу | ",
                  "grant_table - предоставить права на таблицу \n",
                  "export_DB - экспортировать БД",
                  "export_table - экспортировать данные таблицы (в csv)\n",
                  "-" * 130
                  )

        if q == "create_DB":
            dtb = input("имя новой БД: ")
            self.dtbs.create_database(str(dtb))
            input()

        if q == "create_table":
            create_table()
            input()

        if q == "view_DB":
            result = self.dtbs.view_database()
            for row in result:
                print(*row)
            input()

        if q == "drop_DB":
            dtb = input("name database: ")
            result = self.dtbs.drop_database(dtb)
            print(result)
            input()

        if q == "drop_table":
            dtb = input("name database: : ")
            table = input("name table: ")
            q = self.dtbs.view_table_database(dtb)
            for rows in q:
                if table not in rows:
                    continue
                else:
                    result = self.dtbs.drop_table(dtb, table)
                    print(result)
                input()

        if q == "view_table":
            dtb = input("name database: ")
            result = self.dtbs.view_table_database(dtb)
            for rows in result:
                print("таблица: ", *rows)
            input()

        if q == "view_structure":
            dtb = input("name database: ")
            name_table = input("table name: ")
            result = self.dtbs.view_structure(dtb, name_table)
            if result is None:
                print("Таблица не найдена")
                return
            print("_ " * 30)
            print(f"database {dtb}, таблица {name_table}")
            for rows in result:
                print(rows)
            print("_ " * 30)
            input()

        if q == "view_role":
            result = self.dtbs.view_role()
            if result is None:
                print("База не найдена")
                return
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
            result = self.dtbs.view_user()
            if result is None:
                print("нет доступа")
            else:
                print("*" * 30)
                for user in result:
                    print(user[0])
                print("*" * 30)
            input()

        if q == "create_user":
            user = input("Новый пользователь: ")
            pswrd = input("Пароль нового пользователя: ")
            result = self.dtbs.create_new_user(str(user), pswrd)
            print(result)
            input()

        if q == "delete_user":
            user = input("Удаляемый пользователь: ")
            result = self.dtbs.delete_user(user)
            print(result)
            input()

        if q == "grant_DB":
            database_name = input("имя базы: ")
            username = input("имя пользователя: ")
            print("Привилегии", config.privilegy_DB)
            privileges = input('Тип привилегий: ')
            if privileges not in config.privilegy_DB:
                print("некорректная привилегия")
                return
            else:
                result = self.dtbs.grant_privileges(database_name, username, privileges)
                print(result)
            input()

        if q == "grant_table":
            username = input("имя пользователя: ")
            dtb = input("имя базы: ")
            table = input("название таблицы: ")
            print("Привилегии", config.privilegy_table)
            privileges = input('Тип привилегий: ')
            if privileges not in config.privilegy_table:
                print("некорректная привилегия")
                return
            else:
                result = self.dtbs.grant_privileges_table(username, dtb, table, privileges)
                print(result)
            input()

        if q == "export_DB":
            db_name = input("имя базы: ")
            output_file = input("имя выходного файла: ")
            result = self.dtbs.export_database(db_name, output_file)
            print(result)

        if q == "export_table":
            db_name = input("имя базы: ")
            table = input("имя таблицы: ")
            output_file = input("имя выходного файла: ")
            result = self.dtbs.export_data_table(db_name, table, output_file)
            print(result)


if __name__ == "__main__":
    while True:
        testObj = Operation()

