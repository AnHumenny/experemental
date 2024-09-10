import datetime
import time
import pymysql
import requests
from bs4 import BeautifulSoup
import io
from PIL import Image
from random import choice
import matplotlib.pyplot as plt

abs_path = "/bot_current/image/"

check_list = ["USD", "EUR", "RUB", "CNY"]

list_url = [
    "https://myfin.by/currency/torgi-na-bvfb/kurs-dollara",
    "https://myfin.by/currency/torgi-na-bvfb/kurs-euro",
    "https://myfin.by/currency/torgi-na-bvfb/kurs-rublya",
    "https://myfin.by/currency/torgi-na-bvfb/kurs-cny"
]


def get_currency_rate(temp):
    if temp == "USD":
        url = list_url[0]
    if temp == "EUR":
        url = list_url[1]
    if temp == "RUB":
        url = list_url[2]
    if temp == "CNY":
        url = list_url[3]
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    curs = soup.find("div", class_="currency-detailed-change-card__changes").text

    return curs


def actual_img(temp):
    day = []
    curr = []
    actual = []
    conn = pymysql.connect(host="localhost",
                           user="admin",
                           password="1qazxcde3",
                           database="orm_5"
                           )
    cursor = conn.cursor()
    query = f'SELECT actual_current, date, type_current FROM stat_current WHERE type_current = %s ORDER BY date ASC LIMIT 7'
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
    buf = io.BytesIO()
    figure = plt.gcf()
    plt.title("Стат за 7 дней")
    plt.xlabel('День')
    plt.ylabel(f"Курс")
    random_color = ['magenta', 'red', 'black', 'green', 'blue', 'purple', 'brown']
    random_marker = ['o', 'D', 's', 'd', '+', '*', 'p', '4', '3', '2', '1', '^', 'v']
    random_linestyle = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']
    plt.plot(day, curr, label=temp + " ", color=choice(random_color),
             linestyle=choice(random_linestyle), marker=choice(random_marker))
    plt.grid(True)
    plt.legend(loc='upper left')

    def fig2img(fig):
        fig.savefig(buf)
        buf.seek(0)
        img = Image.open(buf)
        time.sleep(1)

        return img

    time.sleep(1)
    img = fig2img(figure)
    time.sleep(1)
    img.save(f'{abs_path}image_{temp}.png')
    plt.close()
    del day
    del curr
    del actual
    return


def insert_into():
    url = [
        ["https://myfin.by/currency/torgi-na-bvfb/kurs-dollara"],
        ["https://myfin.by/currency/torgi-na-bvfb/kurs-euro"],
        ["https://myfin.by/currency/torgi-na-bvfb/kurs-rublya"],
        ["https://myfin.by/currency/torgi-na-bvfb/kurs-cny"]
    ]
    path_info = "currency-detailed-change-card__value"
    path_marker = "currency-detailed-change-card__currency"
    # Получаем дату
    current_date = datetime.date.today().isoformat()

    for rows in url:
        buf = io.BytesIO()
        figure = plt.gcf()
        print(rows)
        response = requests.get(*rows)
        soup = BeautifulSoup(response.content, "html.parser")
        result = soup.find("div", class_=path_info).text
        curs = soup.find("span", class_=path_marker).text
        res = result.strip()
        cur = curs[-3:].strip()
        conn = pymysql.connect(host="localhost",
                               user="admin",
                               password="1qazxcde3",
                               database="orm_5"
                               )
        cursor = conn.cursor()
        sql = "insert into stat_current(actual_current, date, type_current) values( %s, %s, %s )"
        cursor.execute(sql, (res, current_date, cur))
        conn.commit()
        query = f'SELECT actual_current, date, type_current FROM stat_current WHERE type_current = %s ORDER BY date ASC LIMIT 5'
        cursor.execute(query, (cur,))
        print(f"подгружаем {cur}")
        print('res', cur)
        result = cursor.fetchall()
        day = []
        curr = []
        actual = []
        for row in result:
            actual.append(str(row[0]))
            curr.append(float(row[0]))
            day.append(str(row[1]))
        print("day", day)
        print("curr", curr)
        conn.close()
        print("ok!")
        time.sleep(3)

        plt.title("Стат за 7 дней")
        plt.xlabel('День')
        plt.ylabel(f"Курс")
        random_color = ['magenta', 'red', 'black', 'green', 'blue', 'purple', 'brown']
        random_marker = ['o', 'D', 's', 'd', '+', '*', 'p', '4', '3', '2', '1', '^', 'v']
        random_linestyle = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']
        plt.plot(day, curr, label=cur + " ", color=choice(random_color),
                 linestyle=choice(random_linestyle), marker=choice(random_marker))
        plt.grid(True)
        plt.legend(loc='upper left')

        def fig2img(fig):
            fig.savefig(buf)
            buf.seek(0)
            img = Image.open(buf)
            time.sleep(2)
            return img

        img = fig2img(figure)
        time.sleep(5)
        day.clear()
        curr.clear()
        actual.clear()
        img.save(f'/home/joymaster/PycharmProjects/current/bot_current/image/image_all.png')
    plt.close()


def insert_exchange():
    for row in list_url:
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
        conn = pymysql.connect(host="localhost",
                               user="admin",
                               password="1qazxcde3",
                               database="orm_5"
                               )
        cursor = conn.cursor()
        query = "insert into stat_current(actual_current, date, type_current) values( %s, %s, %s )"
        cursor.execute(query, (actual_current, current_date, type_current))
        print(f"OK! {type_current}")
        conn.commit()
        conn.close()
        time.sleep(5)

