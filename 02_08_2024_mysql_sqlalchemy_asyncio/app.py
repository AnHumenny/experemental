import asyncio
from repository import Repo


#выбрать логины в БД
async def view_user_name():
    result = await Repo.view_all_name()
    print(result)
    for row in result:
        print(row)


#данные по id
async def select_id():
    ssid = input("id: ")
    result = await Repo.view_person(ssid)
    for row in result:
        print(row)


#данные по всем users
async def view_all_about_user():
    temp = "user"
    result = await Repo.view_all(temp)
    for row in result:
        print(f"{row[0]:5} | {row[1]:20} | {row[2]:30} | {row[3]:20}")


#данные по всем Project
async def view_all_about_project():
    temp = "project"
    result = await Repo.view_all(temp)
    for row in result:
        print(f"{row[0]:5} | {row[1]:20} | {row[2]:30} | {row[3]:20}")


#данные по локации
async def select_location():
    map_ = input("имя: ")
    result = await Repo.view_location(map_)
    for row in result:
        print(*row)


#обновить User
async def update_user():
    temp = "user"
    l = []
    ssid = int(input("id: "))
    l.append(ssid)
    name = input('name: ')
    l.append(name)
    full_name = input('full_age: ')
    l.append(full_name)
    age = int(input('age: '))
    l.append(age)
    await Repo.update_all_info(l, temp)


#обновить Project
async def update_project():
    temp = "project"
    l = []
    ssid = int(input("id: "))
    l.append(ssid)
    map = input('map: ')
    l.append(map)
    location = input('location: ')
    l.append(location)
    name = input('name: ')
    l.append(name)
    await Repo.update_all_info(l, temp)


#добавить в User
async def insert_user():
    temp = "user"
    name = input('name: ')
    l = [0]
    l.append(name)
    full_name = input('full_age: ')
    l.append(full_name)
    age = int(input('age: '))
    l.append(age)
    result = await Repo.insert_into_all(l, temp)
    print(result)


#добавить в Project
async def insert_project():
    temp = "project"
    l = [0]
    map = input('map: ')
    l.append(map)
    location = input('location: ')
    l.append(location)
    name = input('name: ')
    l.append(name)
    result = await Repo.insert_into_all(l, temp)
    print(result)


#удалить в User
async def delete_user():
    temp = "user"
    ssid = input("id: ")
    result = await Repo.delete_all_id(ssid, temp)
    print(result)


#удалить в Project
async def delete_project():
    temp = "project"
    ssid = input("id: ")
    result = await Repo.delete_all_id(ssid, temp)
    print(result)


#search on age
async def search_age():
    check_symbol = ["<", ">", "="]
    age = int(input("age: "))
    symbol = input("symbol: ")
    if symbol in check_symbol:
        result = await Repo.search_age(symbol, age)
        for row in result:
            print(row)
    else:
        print("Incorrect type!")


if __name__ == "__main__":
    def start():
        query = input("выбор: view | id | all_user | all_project | loc\n"
                      "update_user | update_project | insert_user | insert_project\n"
                      "delete_user | delete_project | search_age:: ")
        if query == "view":
            asyncio.run(view_user_name())
        if query == "id":
            asyncio.run(select_id())
        if query == "all_user":
            asyncio.run(view_all_about_user())
        if query == "all_project":
            asyncio.run(view_all_about_project())
        if query == "loc":
            asyncio.run(select_location())
        if query == "update_user":
            asyncio.run(update_user())
        if query == "update_project":
            asyncio.run(update_project())
        if query == "insert_user":
            asyncio.run(insert_user())
        if query == "insert_project":
            asyncio.run(insert_project())
        if query == "delete_user":
            asyncio.run(delete_user())
        if query == "delete_project":
            asyncio.run(delete_project())
        if query == "search_age":
            asyncio.run(search_age())


    start()
