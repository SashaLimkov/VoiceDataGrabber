import os
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext

from TatSpeaks.settings import BASE_DIR
from bot.config.loader import bot
from bot.utils.message_worker import try_edit_message, try_send_voice

from backend.services.originals import get_less_answered_original, get_original_by_pk, create_user_answer, \
    get_original_from_first_batch
from bot.data import text_data as td
from bot.states.Answering import Answers
from bot.utils import deleter
from bot.keyboards import inline as ik


async def start_answering(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    done_batch = data.get("done_batch", False)
    if not done_batch:
        statement = get_original_from_first_batch(telegram_id=user_id)
        if not statement:
            await state.update_data(done_batch=True)
            statement = get_less_answered_original(telegram_id=user_id)
    else:
        statement = get_less_answered_original(telegram_id=user_id)

    await state.update_data(current_statement=statement.pk)
    text = td.ANSWER_TO.format(statement=statement.string)
    await try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        state=state,
        keyboard=0
    )
    await Answers.GET_VOICE.set()


async def get_user_voice(message: types.Voice, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = message.chat.id
    await deleter.try_delete_message(chat_id=user_id, message_id=message.message_id)
    current_statement = get_original_by_pk(data.get("current_statement"))
    text = td.ANSWER_TO.format(statement=current_statement.string)
    await Answers.MAIN.set()
    await try_send_voice(
        user_id=user_id,
        text=text,
        voice=message.voice.file_id,
        keyboard=await ik.get_answering_menu(),
        state=state
    )


async def reanswer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_message_id = data.get("main_message_id", False)
    user_id = call.message.chat.id
    statement = get_original_by_pk(data.get("current_statement")).string
    text = td.ANSWER_TO.format(statement=statement)
    await try_edit_message(
        message=call.message,
        user_id=user_id,
        text=text,
        main_message_id=main_message_id,
        state=state,
        keyboard=0
    )
    await Answers.GET_VOICE.set()


async def next_statement(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file_id = call.message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    main_message_id = data.get("main_message_id", False)
    current_statement_pk = data.get("current_statement")
    statement = get_original_by_pk(pk=current_statement_pk)
    user_id = call.message.chat.id
    file_name = f"{statement.string} {user_id}.mp3"
    await bot.download_file(file_path, file_name)
    downloaded_file_path = os.path.join(BASE_DIR, file_name)
    create_user_answer(
        current_statement_pk=current_statement_pk,
        user_id=user_id,
        file=downloaded_file_path,
        file_name=file_name)
    os.remove(downloaded_file_path)
    await start_answering(call=call, state=state)

# async def handle_file(file, file_name: str, path: str):
#     Path(f"{path}").mkdir(parents=True, exist_ok=True)
#     await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")
