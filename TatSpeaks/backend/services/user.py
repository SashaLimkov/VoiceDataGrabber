from backend.models import TelegramUser


def create_user(name, telegram_id: int, age):
    return TelegramUser.objects.create(
        name=name,
        chat_id=telegram_id,
        age=age
    )


def get_profile_by_telegram_id(telegram_id: int) -> TelegramUser:
    """Возвращает Profile пользователя по telegram_id"""
    return TelegramUser.objects.filter(chat_id=telegram_id).first()
