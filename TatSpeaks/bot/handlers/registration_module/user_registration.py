import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import deep_linking

from backend.services import user as user_services
from bot.keyboards import inline as ik
from bot.states.Registration import UserRegistration
from bot.utils import deleter
from bot.data import text_data as td
from bot.utils.message_worker import try_edit_message, try_send_message


async def start_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    text = td.REGISTRATION
    if main_message_id:
        await try_edit_message(
            message=message,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=await ik.get_start_registration_keyboard(),
            state=state,
        )
    else:
        await try_send_message(
            message=message,
            user_id=user_id,
            text=text,
            keyboard=await ik.get_start_registration_keyboard(),
            state=state,
        )


async def get_main_registration_menu(call: types.CallbackQuery, state: FSMContext):
    await get_registration_menu(message=call.message, state=state)


async def get_registration_menu(message: types.Message, state: FSMContext):
    await UserRegistration.MENU.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    text = td.REGISTRATION_MAIN
    fio = data.get("fio", False)
    age = data.get("age", False)
    text = text.format(
        fio=fio if fio else "",
        age=age if age else "",
    )
    if fio and age:
        await try_edit_message(
            message=message,
            user_id=user_id,
            text=text,
            keyboard=await ik.get_user_registration_menu(done=True),
            main_message_id=main_message_id,
            state=state,
        )
        return
    await try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        keyboard=await ik.get_user_registration_menu(),
        main_message_id=main_message_id,
        state=state,
    )


async def press_user_fio_or_phone(
        call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.from_user.id
    if callback_data["action"] == "1":
        await UserRegistration.FIO.set()
        text = td.REGISTRATION_FIO
        await try_edit_message(
            message=call,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=0,
            state=state,
        )
    else:
        await UserRegistration.AGE.set()
        text = td.REGISTRATION_AGE
        await try_edit_message(
            message=call,
            user_id=user_id,
            text=text,
            main_message_id=main_message_id,
            keyboard=0,
            state=state,
        )


async def get_user_fio(message: types.Message, state: FSMContext):
    await state.update_data({"fio": message.text})
    await message.delete()
    await get_registration_menu(message=message, state=state)


async def get_user_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({"age": message.text})
        await message.delete()
        await get_registration_menu(message=message, state=state)
    else:
        pass


async def confirm_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    fio = data.get("fio", False)
    age = data.get("age", False)
    text = td.MAIN_MENU
    user = user_services.create_user(name=fio, age=age, telegram_id=user_id)
    await try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        state=state,
        keyboard=await ik.get_main_menu()
    )