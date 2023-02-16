from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistration(StatesGroup):
    MENU = State()
    FIO = State()
    AGE = State()
