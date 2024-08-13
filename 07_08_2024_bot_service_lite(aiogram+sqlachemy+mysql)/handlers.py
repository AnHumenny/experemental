from aiogram import types, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list
from aiogram.utils.keyboard import InlineKeyboardBuilder
import base64
from aiogram.utils.markdown import hlink
import time
import lists
from aiogram.fsm.state import StatesGroup, State
import keyboards
from repository import Repo
from time import sleep


router = Router()


class SelectInfo(StatesGroup):
    register_user = State()
    view_azs = State()
    view_man = State()
    view_bs_number = State()
    view_bs_address = State()
    view_action = State()
    select_action = State()


class Registred:
    admin_OK = False
    user_OK = False
    available_user_names = []
    login = ''
    name = ''
    count = 0


@router.message(StateFilter(None), Command("start"))
async def start_handler(msg: Message, state=FSMContext):
    await msg.answer("Привет! \n")
    await msg.answer(
        text="Знаешь как зайти? :)",
        reply_markup=keyboards.make_row_keyboard(['xxxxx'])
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
                if result.status == "admin":
                    Registred.admin_OK = True
                if result.tg_id in lists.access:
                    Registred.user_OK = True
                    Registred.login = result.login
                    Registred.name = result.name
                    l = [0, result.login, msg.date, "зашёл в чат"]
                    await Repo.insert_into_date(l)
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
        if Registred.admin_OK is True:
            content = as_list(*lists.adm_help)
            await msg.answer(**content.as_kwargs())


#список контактов по МТС
@router.message(F.text, Command('contact'))
async def message_handler(msg: Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await msg.answer(
            text=f"недостаточно прав доступа :("
        )
        return
    else:
        content = as_list(*lists.contact)
        await msg.answer(**content.as_kwargs())


#поиск АЗС по номеру
@router.message(StateFilter(None), Command("view_azs"))
async def view_namber_azs(msg: Message, state: FSMContext):
    if Registred.login in lists.id_user and Registred.user_OK is True:  # проверка статуса
        await msg.answer(
            text=f"номер АЗС",
            reply_markup=keyboards.make_row_keyboard(["АЗС-52"])
        )
        await state.set_state(SelectInfo.view_azs)
    else:
        await msg.answer(
            text=f"недостаточно прав доступа :(",
        )
        return
    await state.set_state(SelectInfo.view_azs)
@router.message(SelectInfo.view_azs)
async def select_azs(msg: Message, state: FSMContext):
    if msg.text is None:
        await msg.answer(f"Фигня  с данными :(")
        await state.clear()
        return
    else:
        number = msg.text.strip()
        if number != '':
            answer = await Repo.select_azs(number)
            try:
                await msg.answer(f"{answer.ip} \n {answer.address} \n {answer.tip} \n "
                                 f"{answer.region} \n {answer.comment}")

                response = hlink('Яндекс-карта', f'https://yandex.by/maps/?ll={answer.geo}&z=16')
                await msg.answer(f"{response}")
                l = [0, Registred.name, msg.date, f"посмотрел данные по {number}"]
                await Repo.insert_into_date(l)
                await state.clear()
            except AttributeError:
                print('Пустой запрос')
                await msg.answer(text=f"Нет такой АЗС :(")
                return


#поиск BS по number
@router.message(StateFilter(None), Command("view_bs_id"))
async def view_namber_bs(msg: Message, state: FSMContext):
    if Registred.login in lists.id_user and Registred.user_OK is True:  # проверка статуса
        await msg.answer(
            text=f"номер БС",
            reply_markup=keyboards.make_row_keyboard(["474"])
        )
        await state.set_state(SelectInfo.view_bs_number)
    else:
        await msg.answer(
            text=f"недостаточно прав доступа :(",
        )
        return
    await state.set_state(SelectInfo.view_bs_number)
@router.message(SelectInfo.view_bs_number)
async def select_bs_id(msg: Message, state: FSMContext):
    if msg.text is None:
        await msg.answer(f"Фигня  с данными :(")
        await state.clear()
        return
    else:
        number = msg.text.strip()
        answer = await Repo.select_bs_number(number)
        await msg.answer(f"{answer.address}\n{answer.comment}")
        l = [0, Registred.name, msg.date, f"посмотрел данные по БС - {number}"]
        await Repo.insert_into_date(l)
        await state.clear()
        if answer is None:
            await msg.answer(text=f"Нет такой БС :(")
            await state.clear()
            return
        return


#поиск BS по street
@router.message(StateFilter(None), Command("view_bs_address"))
async def view_address_bs(msg: Message, state: FSMContext):
    if Registred.login in lists.id_user and Registred.user_OK is True:  # проверка статуса
        await msg.answer(
            text=f"адреc БС(улица)",
            reply_markup=keyboards.make_row_keyboard(["Телегина"])
        )
        await state.set_state(SelectInfo.view_bs_address)
    else:
        await msg.answer(
            text=f"недостаточно прав доступа :(",
        )
        return
    await state.set_state(SelectInfo.view_bs_address)
@router.message(SelectInfo.view_bs_address)
async def select_bs_ad(msg: Message, state: FSMContext):
    if msg.text is None:
        await msg.answer(f"Фигня  с данными :(")
        await state.clear()
        return
    else:
        street = msg.text.strip()
        if street in lists.block_word:
            await msg.answer(f" Некорректный запрос ")
            await state.clear()
            return
        answer = await Repo.select_bs_address(street)
        if answer is not None:
            for row in answer:
                await msg.answer(f"\n{row.number} \n{row.address} \n{row.comment}  ")
            l = [0, Registred.name, msg.date, f"посмотрел данные по - {street}"]
            await Repo.insert_into_date(l)
            await state.clear()
        if answer is None:
            print('Пустой запрос')
            await msg.answer(text=f"Нет такой БС :(")
            await state.clear()
            return
        return


#выборка действий пользователя
@router.message(StateFilter(None), Command("view_action"))
async def view_action_select(msg: Message, state: FSMContext):
    print('help', Registred.login, Registred.user_OK)
    if Registred.login in lists.log_admin and Registred.admin_OK is True:  # проверка статуса
        await msg.answer(
            text=f"Пользовательские запросы(количество): ",
            reply_markup=keyboards.make_row_keyboard(["15"])
        )
        await state.set_state(SelectInfo.select_action)
    else:
        await msg.answer(
            text=f"недостаточно прав доступа :(",
        )
        return
    await state.set_state(SelectInfo.select_action)
@router.message(SelectInfo.select_action)
async def select_action_user(msg: Message, state: FSMContext):
    if msg.text is None:
        await msg.answer(f"Фигня  с данными :(")
        await state.clear()
        return
    else:
        number = msg.text
        print(number)
        if int(number) > 15:
            await msg.answer(f"{number} > 15, попробуй ещё раз :)")
            await state.clear()
            return
        answer = await Repo.select_action(number)
        l = []
        for row in answer:
            l.append(f"{row.login}, {row.action}, {row.date}")
        for row in l:
            await msg.answer(f"{row}")
        await state.clear()
    return

@router.message(Command("view_man"))
async def cmd_random(message: types.Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await message.answer(
            text=f"недостаточно прав доступа :("
        )
        return
    else:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="HUAWEI-5100",
            callback_data="1")
        )
        builder.add(types.InlineKeyboardButton(
            text="Ubiquti",
            callback_data="2")
        )
        builder.row(types.InlineKeyboardButton(
            text="D-Link DGS-3000/3120",
            callback_data="3")
        )
        builder.add(types.InlineKeyboardButton(
            text="Cisco точки доступа ",
            callback_data="4")
        )
        builder.row(types.InlineKeyboardButton(
            text="Mikrotik 3G стартовая конфигурация",
            callback_data="5")
        )
        builder.row(types.InlineKeyboardButton(
            text="MikroTik 3G/4G сеть",
            callback_data="6")
        )
        builder.add(types.InlineKeyboardButton(
            text="MikroTik FTTX",
            callback_data="7")
        )
        builder.row(types.InlineKeyboardButton(
            text="Основные команды d-link",
            callback_data="8")
        )
        await message.answer(
            "Что надо?",
            reply_markup=builder.as_markup()
        )


@router.callback_query(F.data == "1")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(1)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел данные по HUAWEI-5100"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "2")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(2)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел данные по Ubiquti"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "3")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(3)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел данные по D-Link DGS-3000/3120"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "4")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(4)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел данные по Cisco точки доступа"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "5")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(5)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел данные по Mikrotik 3G стартовая конфигурация"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "6")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(6)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"MikroTik 3G/4G сеть"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "7")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(7)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел данные по MikroTik FTTX"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")


@router.callback_query(F.data == "8")
async def send_random_value(callback: types.CallbackQuery):
    answer = await Repo.select_manual(8)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    l = [0, Registred.name, time_str, f"посмотрел Основные команды d-link"]
    await Repo.insert_into_date(l)
    await callback.message.answer(f"{answer.tip} \n {answer.comment}")
