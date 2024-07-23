from create_table import create_tables


def create_new_base():
    print("1 - добавить таблицу \n 2 - прервать")
    num = int(input("1, 2: "))
    if num == 1:
        create_tables()
    if num == 2:
        print('exit!')


create_new_base()
