import sqlite3
import os



def start():
    name_db = input('name DB: ')
    find_db = os.path.isfile(name_db+'.db')
    print(find_db)
    if find_db is False:
        conn = sqlite3.connect(name_db+'.db')
        print(f'база данных {name_db}.db создана!')
        table_name = input('имя таблицы: ')
        conn.execute(f'''
                     CREATE TABLE IF NOT EXISTS {table_name}(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name VARCHAR(20),
                     full_name VARCHAR(20),
                     age INTEGER(2)
                     );
                     ''')
        print(f'the tables {table_name} has been added!')
        conn.commit()
        conn.close()


def insert_into():
    name_db = input('name DB: ')
    name_table = input('name table: ')
    conn = sqlite3.connect(name_db+'.db')
    all_tables = []
    find_table = conn.execute(f'SELECT name FROM sqlite_sequence')
    for row in find_table:
        all_tables.append(row)
        if find_table not in all_tables:
            print('the table is missing!')
            answer = input('create a table? (yes/no): ')
            if answer == 'yes':
                add_tables()
            if answer == 'no':
                print('Exit!')
                return

        else:
            l = int(input('количество строк: '))
            data = [[input() for i in range(3)] for j in range(l)]
            print(data)
            sql = f'''INSERT INTO {name_table} (name, full_name, age) VALUES (?, ?, ?)'''
            with conn:
                conn.executemany(sql, data)
                print('Added!')

    conn.commit()
    conn.close()


def wiev_info():
    name_db = input('name DB: ')
    name_table = input('name table: ')
    conn = sqlite3.connect(name_db+'.db')
    result = conn.execute(f'SELECT * FROM {name_table}')
    for row in result:
        print(*row)
    conn.close()

def add_tables():
    name_db = input('name DB: ')
    name_table = input('name table: ')
    conn = sqlite3.connect(name_db+'.db')
    conn.execute(f'''
                 CREATE TABLE IF NOT EXISTS {name_table}(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name VARCHAR(20),
                     full_name VARCHAR(20),
                     age INTEGER(2)
                 );
                 ''')
    print(f'the tables {name_table} has been added!')
    conn.commit()
    conn.close()


def view_tables():
    base_name = input('name DB: ')
    conn = sqlite3.Connection(base_name+'.db')
    select_tables = conn.execute(f'SELECT name FROM main')
    for row in select_tables:
        print(*row)


n = int(input("1-создать БД, 2-добавить инфу, 3-посмотреть существующую информацию, 4-добавить таблицу,"
              "5-посмотреть таблицы:"))
if n == 1:
    start()
if n == 2:
    insert_into()
if n == 3:
    wiev_info()
if n == 4:
    add_tables()
if n == 5:
    view_tables()





