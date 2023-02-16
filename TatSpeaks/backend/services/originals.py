import random

from django.core.files import File
from django.db import IntegrityError

from backend.models import OriginalString, UserAnswers, FirstBatch
from backend.services.user import get_profile_by_telegram_id


def create_original(original_string: str):
    try:
        r = OriginalString.objects.create(string=original_string)
        return r
    except IntegrityError:
        return OriginalString.objects.filter(string=original_string).first()


def get_original_from_first_batch(telegram_id: int):
    r = FirstBatch.objects.order_by("original_string__answers").all()
    originals = (original for original in r)
    original = next(originals)
    if is_answered_by_user(telegram_id=telegram_id, current_statement_pk=original.original_string.pk):
        r = is_answered_by_user(telegram_id=telegram_id, current_statement_pk=original.original_string.pk)
        while r:
            try:
                original = next(originals)
            except StopIteration:
                return False
        return original.original_string
    return original.original_string


def get_less_answered_original(telegram_id: int) -> OriginalString | bool:
    originals = OriginalString.objects.order_by("answers").all()
    originals_gen = (original for original in originals)
    selected = next(originals_gen)
    print(selected)
    if is_answered_by_user(telegram_id=telegram_id, current_statement_pk=selected.pk):
        while not is_answered_by_user(telegram_id=telegram_id, current_statement_pk=selected.pk):
            try:
                selected = next(originals_gen)
            except StopIteration:
                return False
        return selected
    return selected


def get_original_by_pk(pk: int) -> OriginalString:
    return OriginalString.objects.filter(pk=pk).first()


def create_user_answer(current_statement_pk, user_id, file, file_name):
    original = get_original_by_pk(current_statement_pk)
    user = get_profile_by_telegram_id(user_id)
    import mutagen
    audio_info = mutagen.File(file).info

    with open(file, "rb") as f:
        print(f)
        obj = UserAnswers(
            original_string=original,
            user=user,
            audio_len=audio_info.length,
        )
        obj.audio_file.save(
            file_name,
            File(f))
        obj.save()


def is_answered_by_user(telegram_id: int, current_statement_pk: int) -> bool:
    user = get_profile_by_telegram_id(telegram_id=telegram_id)
    user_answer = UserAnswers.objects.filter(user=user.pk, original_string__pk=current_statement_pk).first()
    return True if user_answer else False


def get_first_batch_to_fill():
    r = OriginalString.objects.order_by('?').all()
    return r[:100]


def create_first_barch(original: OriginalString):
    return FirstBatch.objects.create(
        original_string=original
    )
#
# if __name__ == '__main__':
#     is_answered_by_user(telegram_id=390959255, current_statement_pk=3)
