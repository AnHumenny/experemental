import sqlite3
import os

path_base = 'base/'


def create_database():
    basename = input('name DB: ')
    find_base = os.path.isfile(path_base + basename+'.db')
    if find_base is False:
        print('the base never was been!')
        print(f'create new base {basename} (yes/no)')
        question = input('yes/no: ')
        if question == 'no':
            print('exit!')
            return
        if question == 'yes':
            conn = sqlite3.connect(path_base + basename+'.db')
            print(f'database {basename} are created!')
            conn.commit()
            conn.close()


def insert_data():
    basename = input('name DB: ')
    find_base = os.path.isfile(path_base + basename + '.db')
    if find_base is False:
        print('the base never was been!')
        return
    type_of_insert = input('people, groceries: ')
    table_name = input('table_name: ')
    n = int(input('numbers of line: '))
    conn = sqlite3.connect(path_base + basename + '.db')
    if type_of_insert == 'people':
        data = [[input(f'pos {i}: ') for i in range(3)] for j in range(n)]
        sql = f"INSERT INTO {table_name} (name, full_name, age) VALUES (?, ?, ?);"
        with conn:
            conn.executemany(sql, data)
        conn.commit()
        conn.close()
    if type_of_insert == 'groceries':
        data = [[input(f'pos {i}: ') for i in range(3)] for j in range(n)]
        sql = f"INSERT INTO {table_name} (groceries, price, discount) VALUES (?, ?, ?);"
        with conn:
            conn.executemany(sql, data)
        conn.commit()
        conn.close()


def check_base():
    name_base = input('name DB: ')
    find_base = os.path.isfile(path_base + name_base+'.db')
    if find_base is True:
        print(f'{name_base} is found!')
        question = input("create tables (yes/no) : ")
        if question == 'no':
            print('exit! ')
            return
        if question == 'yes':
            create_tables(name_base)
    else:
        print(f'create new base {name_base}? (yes/no): ')
        n = input("yes/no : ")
        if n == 'no':
            print('exit!')
            return
        if n == 'yes':
            conn = sqlite3.connect(path_base + name_base + '.db')
            print(f'database {name_base} are created!')
            conn.commit()
            conn.close()


def create_tables(name_base):
    table_name = input('table name: ')
    type_of_tables = input('people, groceries: ')
    if type_of_tables == 'groceries':
        create_table_type_groceries(name_base, table_name)
    if type_of_tables == 'people':
        create_table_type_people(name_base, table_name)


def create_table_type_groceries(name_base, table_name):
    conn = sqlite3.connect(path_base + name_base + '.db')
    conn.execute(f'''
                     CREATE TABLE IF NOT EXISTS {table_name}(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     groceries VARCHAR(20),
                     price INTEGER(100),
                     discount INTEGER(10)
                     );
                     '''
                 )
    conn.commit()
    conn.close()

def view_tables_in_base():
    name_base = input('name DB: ')
    table_name = input('table name: ')
    find_base = os.path.isfile(path_base + name_base + '.db')
    if find_base is False:
        print('the base never was been!')
        return
    else:
        conn = sqlite3.connect(path_base + name_base + '.db')
        result = conn.execute(f'''SELECT name FROM {table_name}''')
        for row in result:
            print(row)


def create_table_type_people(name_base, table_name):
    conn = sqlite3.connect(path_base + name_base + '.db')
    conn.execute(f'''
                         CREATE TABLE IF NOT EXISTS {table_name}(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name VARCHAR(20),
                         full_name VARCHAR(20),
                         age INTEGER(100)
                         );
                         '''
                 )
    conn.commit()
    conn.close()


def view_tables():
    name_base = input('name DB: ')
    find_base = os.path.isfile(path_base + name_base + '.db')
    if find_base is False:
        print('the base never was been!')
        return
    else:
        conn = sqlite3.connect(path_base + name_base + '.db')
        result = conn.execute(f'''SELECT * FROM sqlite_master WHERE type='table';''')
        for row in result:
            print(row[1])
        print('are we looking at the records in the tables?')
        question = input('yes/no : ')
        if question == 'no':
            print('exit!')
            return

        if question == 'yes':
            quest = input('name of tables: ')
            result = conn.execute(f'''SELECT * FROM {quest}''')
            for row in result:
                print(*row)


def view_sales():
    basename = input('name DB: ')
    find_base = os.path.isfile(path_base + basename + '.db')
    if find_base is False:
        print('base unknown!')
        return
    table_name = input('name table: ')
    conn = sqlite3.connect(path_base + basename + '.db')
    result = conn.execute(f'''
                          SELECT groceries, price, discount FROM {table_name} 
                          ''')
    for row in result:
        print(row[0], 'начальная стоимость: ', row[1], ' Стоимость со скидкой:',  row[1] - (row[1] / 100) * row[2])


def update_info():
    basename = 'base'
    find_base = os.path.isfile(path_base + basename + '.db')
    if find_base is False:
        print('base unknown!')
        return
    conn = sqlite3.connect(path_base + basename + '.db')
    name = "ЖОпа"
    sql = f"UPDATE new SET name WHERE id = 1;"

    with conn:
        conn.execute(sql)





n = int(input('number: '))
if n == 1:
    create_database()
if n == 2:
    insert_data()
if n == 3:
    check_base()
if n == 4:
    view_tables_in_base()
if n == 5:
    insert_data()
if n == 6:
    view_tables()
if n == 7:
    view_sales()
if n == 8:
    update_info()
