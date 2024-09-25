import datetime
import time
import matplotlib
import pymysql
import requests
from bs4 import BeautifulSoup
from random import choice
import matplotlib.pyplot as plt
import config


def get_currency_rate(temp):
    if temp == "USD":
        url = config.list_url[0]
    if temp == "EUR":
        url = config.list_url[1]
    if temp == "RUB":
        url = config.list_url[2]
    if temp == "CNY":
        url = config.list_url[3]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    curs = soup.find("div", class_="currency-detailed-change-card__changes").text
    return curs


def actual_img(temp):
    day = []
    curr = []
    actual = []
    conn = pymysql.connect(host=config.host,
                           user=config.user,
                           password=config.password,
                           database=config.database
                           )
    cursor = conn.cursor()
    query = f'SELECT actual_current, date, type_current FROM stat_current WHERE type_current = %s ORDER BY date DESC LIMIT 7'
    cursor.execute(query, (temp,))
    result = cursor.fetchall()
    print(result)
    for row in result:
        actual.append(str(row[0]))
        curr.append(float(row[0]))
        day.append(str(row[1]))
    conn.close()
    print("ok!")
    time.sleep(1)
    plt.title("Стат за 7 дней")
    plt.xlabel('День')
    plt.ylabel("Курс")
    random_color = ['magenta', 'red', 'black', 'green', 'blue', 'purple', 'brown']
    random_marker = ['o', 'D', 's', 'd', '+', '*', 'p', '4', '3', '2', '1', '^', 'v']
    random_linestyle = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']
    axes = plt.subplot(1, 1, 1)
    axes.tick_params(axis='x', labelrotation=55)
    axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))
    plt.plot(day, curr, label=temp + " ", color=choice(random_color),
             linestyle=choice(random_linestyle), marker=choice(random_marker))
    plt.tight_layout()
    plt.grid(True)
    plt.legend(loc='upper left')
    time.sleep(1)
    plt.savefig(f'{config.abs_path}image_{temp}.png')
    time.sleep(1)
    plt.close()
    del day
    del curr
    del actual
    return


def create_all_graf():
    conn = pymysql.connect(host=config.host,
                           user=config.user,
                           password=config.password,
                           database=config.database
                           )
    cursor = conn.cursor()
        for row in config.check_list:
        print('запрашиваем', row)
        query = f'SELECT actual_current, date, type_current FROM stat_current WHERE type_current = %s ORDER BY date DESC LIMIT 7'
        cursor.execute(query, (row,))
        result = cursor.fetchall()
        print("выводим результат запроса", result)
        day = []
        curr = []
        actual = []
        for rows in result:
            actual.append(str(rows[0]))
            curr.append(float(rows[0]))
            day.append(str(rows[1]))
        print("ok!")
        time.sleep(1)
        plt.title("Стат за 7 дней")
        plt.xlabel('День')
        plt.ylabel("Курс")
        random_color = ['magenta', 'red', 'black', 'green', 'blue', 'purple', 'brown']
        random_marker = ['o', 'D', 's', 'd', '+', '*', 'p', '4', '3', '2', '1', '^', 'v']
        random_linestyle = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']
        axes = plt.subplot(1, 1, 1)
        axes.tick_params(axis='x', labelrotation=55)
        axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))
        plt.plot(day, curr, label=row, color=choice(random_color),
                 linestyle=choice(random_linestyle), marker=choice(random_marker))
        plt.tight_layout()
        plt.grid(True)
        plt.legend(loc='upper left')
        time.sleep(1)
        time.sleep(1)
        plt.savefig(f'{config.abs_path}image_all.png')
        del day
        del curr
        del actual
    plt.close()
    conn.close()
    return


def insert_exchange():
    for row in config.list_url:
        response = requests.get(row)
        soup = BeautifulSoup(response.content, "html.parser")
        res = soup.find("div", class_="currency-detailed-change-card__value").text
        label = soup.find("span", class_="currency-detailed-change-card__currency").text
        actual_current = res.strip()
        if len(label) > 4:
            type_current = label[-3:]
        else:
            type_current = label.strip()
        current_date = datetime.date.today().isoformat()
        print(actual_current, current_date, type_current)
        conn = pymysql.connect(host=config.host,
                               user=config.user,
                               password=config.password,
                               database=config.database
                               )
        cursor = conn.cursor()
        query = "insert into stat_current(actual_current, date, type_current) values( %s, %s, %s )"
        cursor.execute(query, (actual_current, current_date, type_current))
        print(f"OK! {type_current}")
        conn.commit()
        conn.close()
        time.sleep(5)
