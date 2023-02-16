from aiogram import Dispatcher
from aiogram.dispatcher import filters

from . import registration_module, main_module
from . import commands


def setup(dp: Dispatcher):
    registration_module.setup(dp)
    main_module.setup(dp)
    dp.register_message_handler(commands.start_command, filters.CommandStart(), state="*")
