from aiogram import Dispatcher, types
from aiogram.dispatcher import filters
from bot.data import callback_data as cd
from . import start_answering
from bot.states.Answering import Answers


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(start_answering.start_answering, filters.Text("start"), state="*")
    dp.register_message_handler(
        start_answering.get_user_voice,
        content_types=types.ContentTypes.VOICE,
        state=Answers.GET_VOICE)
    dp.register_callback_query_handler(
        start_answering.reanswer,
        filters.Text("reanswer"),
        state="*"
    )
    dp.register_callback_query_handler(
        start_answering.next_statement,
        filters.Text("next"),
        state="*"
    )
