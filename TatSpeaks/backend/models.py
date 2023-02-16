from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")


class TelegramUser(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    chat_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    age = models.IntegerField(verbose_name="Возраст пользователя", blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class OriginalString(TimeBasedModel):
    class Meta:
        verbose_name = "Оригинал строки"
        verbose_name_plural = "Оригиналы строк"

    def __str__(self):
        return self.string

    string = models.CharField(
        max_length=255, unique=True, verbose_name="Оригинальная строка"
    )
    answers = models.IntegerField(verbose_name="Сумма ответов", default=0)


class FirstBatch(TimeBasedModel):
    class Meta:
        verbose_name = "Первоочередный набор"

    def __str__(self):
        return f"{self.original_string.string}"

    original_string = models.ForeignKey(OriginalString, on_delete=models.CASCADE, related_name="first_batch")


class UserAnswers(TimeBasedModel):
    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"

    original_string = models.ForeignKey(OriginalString, verbose_name="Оригинал", on_delete=models.CASCADE,
                                        related_name="user_answers")
    user = models.ForeignKey(TelegramUser, verbose_name="Пользователь", on_delete=models.CASCADE,
                             related_name="user_answers")
    audio_file = models.FileField("Аудио", upload_to="sounds")
    audio_len = models.FloatField("Длительность аудио", blank=True)

    def __str__(self):
        return f"{self.original_string.string} - {self.user.name}"


@receiver(post_save, sender=UserAnswers, dispatch_uid="update_upload_to")
def update_upload_to(sender, instance, **kwargs):
    original = instance.original_string
    count_of = len(instance.original_string.user_answers.all())
    original.answers = count_of
    original.save()
