import config

dtb = config.telega_SQL(host=config.host, user=config.user,
                        password=config.password, dtb=config.dtb)

def inputs():
    try:
        yield input("логин, имя, статус, пароль, телефон, емайл, tg_ig: ").split(',')
    except (ValueError, EOFError):
        return

def insert():
    for login, name, status, password, phone, email, tg_id in inputs():
        dtb.check_new_user(login, name, status, password, phone, email, tg_id)
        return


insert()

