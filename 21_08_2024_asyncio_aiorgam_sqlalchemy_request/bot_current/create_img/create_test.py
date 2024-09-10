import datetime
import time
import pymysql
import requests
from bs4 import BeautifulSoup
import io
from random import choice
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

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
    if temp == "USD":
        ind = 0
    if temp == "EUR":
        ind = 1
    if temp == "RUB":
        ind = 2
    if temp == "CNY":
        ind = 3

    conn = pymysql.connect(host="localhost",
                           user="admin",
                           password="1qazxcde3",
                           database="orm_5"
                           )
    cursor = conn.cursor()
    query = f'SELECT actual_current, date, type_current FROM stat_current WHERE type_current = %s ORDER BY date ASC LIMIT 7'
    cursor.execute(query, (temp, ))
    result = cursor.fetchall()
    print(result)
    for row in result:
        actual.append(str(row[0]))
        curr.append(float(row[0]))
        day.append(str(row[1]))
    conn.close()
    print("ok!")
    time.sleep(1)
    img = Image.new('RGB', (600, 400))
    figure = plt.gcf()
    plt.title("Стат за 7 дней")
    plt.xlabel('День')
    plt.ylabel(f"Курс")
    random_color = ['magenta', 'red',  'black', 'green', 'blue', 'purple', 'brown']
    random_marker = ['o', 'D', 's', 'd', '+', '*', 'p', '4', '3', '2', '1', '^', 'v']
    random_linestyle = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']
    plt.plot(day, curr, label=check_list[ind] + " ", color=choice(random_color),
                linestyle=choice(random_linestyle), marker=choice(random_marker))
    plt.grid(True)
    plt.legend(loc='upper left')


    idraw = ImageDraw.Draw(img)
    idraw.rectangle(figure)
    img.save('test1.jpg')
    time.sleep(1)


    img.save(f'{abs_path}image_{temp}.png')
    del day
    del curr
    del actual


actual_img("USD")