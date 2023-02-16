from aiogram.dispatcher.filters.state import StatesGroup, State


class Answers(StatesGroup):
    GET_VOICE = State()
    MAIN = State()
