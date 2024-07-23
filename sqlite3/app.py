import sqlite3 as sl


db_name = input('name BD: ')
table_name = input('table name: ')

conn = sl.connect(db_name+'.db')
conn.execute(f'''
CREATE TABLE IF NOT EXISTS {table_name}(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(30),
full_name VARCHAR(30),
age int(10)
)
''')

conn.commit()
conn.close()