import asyncio
import datetime
import time
import requests
from bs4 import BeautifulSoup
from repository import Repo
import os



async def get_currency_rate():
    # Адрес сайта, с которого мы будем получать данные
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
    # Получаем содержимое страницы
    for row in url:
        response = requests.get(*row)
        soup = BeautifulSoup(response.content, "html.parser")
        res = soup.find("div", class_=path_info).text
        cur = soup.find("span",  class_=path_marker).text
        print(cur)
        if len(cur) > 5:
            cur = cur[23:]
        await Repo.insert_into_ctat_current([0, res.strip(), current_date.strip(), cur.strip()])
        await asyncio.sleep(2)

 #  await asyncio.sleep(30)
    return

if __name__ == "__main__":
    # создаем цикл событий
    loop = asyncio.get_event_loop()
    try:
        # создаем задачи
        task1 = loop.create_task(get_currency_rate())

        # объединяем задачи в группу, для
        # планирования асинхронного выполнения
        group = asyncio.gather(task1)
        # получаем результаты
        print('Ok!')
      #  time.sleep(60)
        loop.run_forever()
      #  print(f'Результаты работы сопрограмм: ') #суммарно
    except:
        print("Упс...")
