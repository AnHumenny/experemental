import requests
from aiogram import types, F, Router, Bot
from aiogram.types import Message, InputFile, BufferedInputFile
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list
from aiogram.utils.keyboard import InlineKeyboardBuilder
import base64
import time
from bs4 import BeautifulSoup
import lists
from aiogram.fsm.state import StatesGroup, State
import keyboards
from repository import Repo
from time import sleep
from parser.parser import bot_pars
from parser.current import get_currency_rate

router = Router()


class SelectInfo(StatesGroup):
    register_user = State()


class Registred:
    user_OK = False
    available_user_names = []
    login = ''
    name = ''
    count = 0


abs_path = "PATH_TO_FILE/"


@router.message(StateFilter(None), Command("start"))
async def start_handler(msg: Message, state=FSMContext):
    await msg.answer("Привет! \n")
    await msg.answer(
        text="Знаешь как зайти? :)",
        reply_markup=keyboards.make_row_keyboard(['xxxxxxx'])
    )
    await state.set_state(SelectInfo.register_user)  # ожидание выбора на виртуальной клавиатуре


#ввод и проверка пароля
@router.message(SelectInfo.register_user)
async def cmd_auth(msg: Message, state: FSMContext):
    if Registred.count > 3:
        Registred.count = 0
    bot = Bot(token=lists.API_TOKEN)
    autent = msg.text.split('|')
    if len(autent) != 2:
        Registred.count += 1
        await msg.answer(
            text=f"Что то за не то с паролем :("
        )
        print("count", Registred.count)
        if Registred.count == 3:
            await msg.answer(
                text="Теперь ждём минуту :("
            )
            l = [0, msg.from_user.id, msg.date, f"{msg.from_user.id} три некорректные авторизации :)"]
            await Repo.insert_into_date(l)
            print("count", Registred.count)
            sleep(60)
        return
    else:
        Registred.count += 1
        auth = msg.text.split("|")
        login = auth[0]
        pswrd = auth[1]
        pass_wrd = pswrd.encode('utf-8')
        password = base64.b64encode(pass_wrd)
        if len(login) == 0 or len(password) < 7:
            await msg.answer(
                text=f"Что то не получилось с паролем :("
            )
            print("count", Registred.count)
            if Registred.count == 3:
                await msg.answer(
                    text="Теперь ждём минуту :("
                    )
                l = [0, msg.from_user.id, msg.date, f"{msg.from_user.id} три неверных попытки подбора пароля :)"]
                await Repo.insert_into_date(l)
                sleep(60)
            await state.clear()
            return
        else:
            result = await Repo.select_pass(login, password, msg.from_user.id)
            if result is None:
                await msg.answer(
                    text=f"Не зашло с паролем :("
                    )
                Registred.count += 1
                if Registred.count == 3:
                    await msg.answer(
                        text="Теперь ждём минуту :("
                        )
                    l = [0, msg.from_user.id, msg.date, f"{msg.from_user.id} три хаотичных пароля :)"]
                    await Repo.insert_into_date(l)
                    sleep(60)
                    await state.clear()
                    return
            else:
                if result.tg_id not in lists.access:
                    await msg.answer(
                        text=f"Упс. Что то не так с данными :("
                    )
                    return
                if result.tg_id in lists.access:
                    Registred.user_OK = True
                    Registred.login = result.login
                    Registred.name = result.name
                await msg.answer(
                    text=f"Набери\n/help, {result.name}"
                    )
                await bot.send_message(408397675, 'В бот зашёл ' + result.name)  #ошибка незакрытой сессии
                await state.clear()
                return


#мануал
@router.message(F.text, Command("help"))
async def cmd_help(msg: Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await msg.answer(
            text=f"Увы. Нет доступа к внутренней информации :("
        )
        return
    else:
        content = as_list(*lists.help)
        await msg.answer(**content.as_kwargs())


@router.message(Command("current_shedule"))
async def cmd_random(message: types.Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await message.answer(
            text=f"недостаточно прав доступа :("
        )
        return
    else:
        builder = InlineKeyboardBuilder()

        builder.row(types.InlineKeyboardButton(
            text="USD",
            callback_data="USD")
        )
        builder.add(types.InlineKeyboardButton(
            text="EURO",
            callback_data="EURO")
        )
        builder.row(types.InlineKeyboardButton(
            text="RUR",
            callback_data="RUR")
        )
        builder.add(types.InlineKeyboardButton(
            text="CNY",
            callback_data="CNY")
        )

        await message.answer(
            "Что надо?",
            reply_markup=builder.as_markup()
        )

@router.callback_query(F.data == "USD")
async def send_current_exchange(callback: types.CallbackQuery):
    url = "https://myfin.by/currency/torgi-na-bvfb/kurs-dollara"
    response_usd = requests.get(url)
    soup = BeautifulSoup(response_usd.content, "html.parser")
    res = soup.find("div", class_="currency-detailed-change-card__changes").text
    ins = soup.find("div", class_="currency-detailed-change-card__value").text
    time_str = time.strftime("%Y-%m-%d")
    l = [0, ins, time_str, "USD"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"Текущий курс доллара\n {res}")


@router.callback_query(F.data == "EURO")
async def send_current_exchange(callback: types.CallbackQuery):
    url = "https://myfin.by/currency/torgi-na-bvfb/kurs-euro"
    response_usd = requests.get(url)
    soup = BeautifulSoup(response_usd.content, "html.parser")
    res = soup.find("div", class_="currency-detailed-change-card__changes").text
    ins = soup.find("div", class_="currency-detailed-change-card__value").text
    time_str = time.strftime("%Y-%m-%d")
    l = [0, ins, time_str, "EURO"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"Текущий курс евро\n {res}")


@router.callback_query(F.data == "RUR")
async def send_current_exchange(callback: types.CallbackQuery):
    url = "https://myfin.by/currency/torgi-na-bvfb/kurs-rublya"
    response_usd = requests.get(url)
    soup = BeautifulSoup(response_usd.content, "html.parser")
    res = soup.find("div", class_="currency-detailed-change-card__changes").text
    ins = soup.find("div", class_="currency-detailed-change-card__value").text
    time_str = time.strftime("%Y-%m-%d")
    l = [0, ins, time_str, "RUR"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"Текущий курс российского рубля\n100 росс.руб. - {res}")


@router.callback_query(F.data == "CNY")
async def send_current_exchange(callback: types.CallbackQuery):
    url = "https://myfin.by/currency/torgi-na-bvfb/kurs-rublya"
    response_usd = requests.get(url)
    soup = BeautifulSoup(response_usd.content, "html.parser")
    res = soup.find("div", class_="currency-detailed-change-card__changes").text
    ins = soup.find("div", class_="currency-detailed-change-card__value").text
    time_str = time.strftime("%Y-%m-%d")
    l = [0, ins, time_str, "CNY"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"Текущий курс юаня\n10 юаней - {res}")


@router.message(Command("current_image"))
async def cmd_rand(message: types.Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await message.answer(
            text=f"недостаточно прав доступа :("
        )
        return
    else:
        builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text="Стат за 7 дней по USD",
        callback_data="USD_graf")
    )

    builder.add(types.InlineKeyboardButton(
        text="Стат за 7 дней по EURO",
        callback_data="EURO_graf")
    )

    builder.row(types.InlineKeyboardButton(
        text="Стат за 7 дней по RUR",
        callback_data="RUR_graf")
    )

    builder.add(types.InlineKeyboardButton(
        text="Стат за 7 дней по CNY",
        callback_data="CNY_graf")
    )

    await message.answer(
        "Что надо?",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "USD_graf")
async def send_current_USD(callback: types.CallbackQuery):
    with open(f'{abs_path}/image_USD.png', 'rb') as file:
        photo = BufferedInputFile(file.read(), 'any_filename')
    await callback.message.answer_photo(photo)


@router.callback_query(F.data == "EURO_graf")
async def send_current_EURO(callback: types.CallbackQuery):
    with open(f'{abs_path}/image_EUR.png', 'rb') as file:
        photo = BufferedInputFile(file.read(), 'any_filename')
    await callback.message.answer_photo(photo)


@router.callback_query(F.data == "RUR_graf")
async def send_current_RUR(callback: types.CallbackQuery):
    with open(f'{abs_path}/image_RUB.png', 'rb') as file:
        photo = BufferedInputFile(file.read(), 'any_filename')
    await callback.message.answer_photo(photo)


@router.callback_query(F.data == "CHY_graf")
async def send_current_CNY(callback: types.CallbackQuery):
    with open(f'{abs_path}/image_CNY.png', 'rb') as file:
        photo = BufferedInputFile(file.read(), 'any_filename')
    await callback.message.answer_photo(photo)
#
# @router.message(F.text, Command('new_current_image'))
# async def message_handler(msg: Message):
#     if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
#         await msg.answer(
#             text=f"недостаточно прав доступа :("
#         )
#         return
#     else:
#         with open('image_USD.png', 'rb') as file:
#             photo = BufferedInputFile(file.read(), 'any_filename')
#         await msg.answer_photo(photo)
#         #await msg.answer_photo(photo='http://gks.by/images/objects/gran/vsig_images/1_780_780_100.jpg') #тест
#  
#
