from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from bot.data import callback_data as cd

__all__ = [
    "get_main_menu",
    "get_answering_menu"
]


async def get_main_menu():
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Начать озвучивать", cd="start"
        )
    )
    return keyboard


async def get_answering_menu():
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    keyboard.add(
        await get_inline_button(
            text="Перезаписать", cd="reanswer"
        )
    )
    keyboard.add(
        await get_inline_button(
            text="Продолжить", cd="next"
        )
    )
    return keyboard
