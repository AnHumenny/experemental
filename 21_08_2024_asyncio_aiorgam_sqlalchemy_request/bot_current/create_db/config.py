#config.py, insert.py - добавление нового пользователя
import pymysql    
import base64


host = host
port = 3306
user = user
password = password
dtb = database
class telega_SQL:
    def __init__(self, host, user, password, dtb):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def add_new_user(self, login, name, status, password, phone, email, tg_id):
        sql = "insert into `users` (login, name, status, password, phone, email, tg_id) values ( %s, %s, %s, %s, %s, %s, %s )"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (login, name, status, password, phone, email, tg_id))
                self.connection.commit()
            return
        except ValueError:
            print('упс :(')
            return
            
    def check_new_user(self, login, name, status, password, phone, email, tg_id):
        query = "SELECT * FROM `users` WHERE login = %s"
        print(login, name, status, password, phone, email, tg_id)
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, (login, ))
                result = cursor.fetchall()
                print(len(result))
                if len(result) == 0:
                    pass_wrd = password.encode('utf-8')
                    password = base64.b64encode(pass_wrd)
                    self.add_new_user(login, name, status, password, phone, email, tg_id)
                else:
                    print('выберите другой логин :(')
            except ValueError:
                print('упс :(')


