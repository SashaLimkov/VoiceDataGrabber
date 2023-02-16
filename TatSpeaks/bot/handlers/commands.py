from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.data import text_data as td
from bot.utils.message_worker import try_edit_message
from bot.utils import deleter
from bot.keyboards import inline as ik


async def start_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    await deleter.try_delete_message(chat_id=user_id, message_id=message.message_id)
    text = td.MAIN_MENU
    await try_edit_message(
        message=message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        state=state,
        keyboard=await ik.get_main_menu()
    )
