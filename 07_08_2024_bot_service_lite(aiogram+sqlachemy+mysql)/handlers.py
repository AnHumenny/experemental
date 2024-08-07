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
    view_action = State()
    select_action = State()


class Registred:
    admin_OK = False
    user_OK = False
    available_user_names = []
    login = ''
    name = ''
    count = 0


named_tuple = time.localtime()  # получаем struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M", named_tuple)


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
    bot = Bot(token=lists.API_TOKEN)
    autent = msg.text.split('|')
    if len(autent) != 2:
        Registred.count += 1
        await msg.answer(
            text=f"Что то за фигня с паролем :("
        )
        if Registred.count == 3:
            await msg.answer(
                text="Теперь ждём минуту :("
            )
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
            if Registred.count == 3:
                await msg.answer(
                    text="Теперь ждём минуту :("
                    )
                sleep(60)
            await state.clear()
            return
        else:
            result = await Repo.select_pass(login, password)
            if result is None:
                await msg.answer(
                    text=f"Не зашло с паролем :("
                    )
                Registred.count += 1
                if Registred.count == 3:
                    await msg.answer(
                        text="Теперь ждём минуту :("
                        )
                    sleep(60)
                    await state.clear()
                    return
            else:
                if result.tg_id not in lists.access:
                    print(lists.access)
                    print('test', result.tg_id)
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
                    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                    l = [0, result.login, time_str, "зашёл в чат"]
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


#юридический адрес организации
@router.message(F.text, Command("address"))
async def message_handler(msg: Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await msg.answer(
            text=f"недостаточно прав доступа :("
        )
        return
    else:
        content = as_list("ООО '          '")
        await msg.reply(**content.as_kwargs())
#куда везти реестры
@router.message(F.text, Command("registers"))
async def message_handler(msg: Message):
    if Registred.login not in lists.id_user and Registred.user_OK is False:  # проверка статуса
        await msg.answer(
            text=f"недостаточно прав доступа :("
        )
        return
    else:
        await msg.answer("        ")
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
        await msg.answer(f"Непорядок  с данными :(")
        await state.clear()
        return
    else:
        number = msg.text
        if number != '':
            answer = await Repo.select_azs(number)
            try:
                await msg.answer(f"{answer.ip} \n {answer.address} \n {answer.tip} \n "
                                 f"{answer.region} \n {answer.comment}")

                response = hlink('Яндекс-карта', f'https://yandex.by/maps/?ll={answer.geo}&z=16')
                await msg.answer(f"{response}")
                time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                l = [0, Registred.name, time_str, f"посмотрел данные по {number}"]
                await Repo.insert_into_date(l)
                await state.clear()
            except AttributeError:
                print('Пустой запрос')
                await msg.answer(text=f"Нет такой АЗС :(")
                return


#поиск man по id
@router.message(StateFilter(None), Command("view_man"))
async def view_man_select(msg: Message, state: FSMContext):
    print(lists.id_user)
    print('help', Registred.login, Registred.user_OK)
    if Registred.login in lists.id_user and Registred.user_OK is True:  # проверка статуса
        content = as_list(*lists.man)
        await msg.answer(**content.as_kwargs())
        await msg.answer(
            text=f"Choose id",
            reply_markup=keyboards.make_row_keyboard(["1"])
        )
        await state.set_state(SelectInfo.view_man)
    else:
        await msg.answer(
            text=f"недостаточно прав доступа :(",
        )
        return
    await state.set_state(SelectInfo.view_man)
@router.message(SelectInfo.view_man)
async def select_man(msg: Message, state: FSMContext):
    if msg.text is None:
        await msg.answer(f"Непорядок  с данными :(")
        await state.clear()
        return
    else:
        number = msg.text
        if number != '':
            answer = await Repo.select_manual(number)
            time_str = time.strftime("%Y-%m-%d %H:%M:%S")
            l = [0, Registred.name, time_str, f"посмотрел в manual данные по id {number}"]
            await Repo.insert_into_date(l)
            try:
                await msg.answer(f"{answer.tip} \n {answer.comment}")
                await state.clear()
            except AttributeError:
                print('Пустой запрос')
                await msg.answer(text=f"ID unknown!")
                return


#внешние ссылки
@router.message(Command("inline_url"))
async def cmd_inline_url(msg: types.Message):
    if Registred.login in lists.id_user and Registred.user_OK is True:  # проверка статуса
        time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        l = [0, Registred.name, time_str, f"заходил в внешние ссылки"]
        await Repo.insert_into_date(l)
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="График",
            url=lists.list_link[0])
        )

        await msg.answer(
            'Куда пойдём?',
            reply_markup=builder.as_markup(),
        )


#выборка действий пользователя
@router.message(StateFilter(None), Command("view_action"))
async def view_action_select(msg: Message, state: FSMContext):
    print('help', Registred.login, Registred.user_OK)
    if Registred.login in lists.log_admin and Registred.admin_OK is True:  # проверка статуса
        await msg.answer(
            text=f"Пользовательсткие запросы(количество): ",
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
        await msg.answer(f"Непорядок  с данными :(")
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
