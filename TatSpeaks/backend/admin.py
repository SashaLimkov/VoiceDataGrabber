import os

from django.contrib import admin
from .models import OriginalString, TelegramUser, UserAnswers, FirstBatch


class UserAnswersInline(admin.StackedInline):
    model = UserAnswers
    fields = ["audio_file", "original_string", "user", "audio_len"]
    readonly_fields = ["original_string", "audio_file", "audio_len", "user"]


class FBAdmin(admin.ModelAdmin):
    readonly_fields = ["original_string"]


class UserAnswersAdmin(admin.ModelAdmin):
    readonly_fields = ["original_string", "user", "audio_file", "audio_len"]


class OriginalAdmin(admin.ModelAdmin):
    inlines = (UserAnswersInline,)


class TelegramUserAdmin(admin.ModelAdmin):
    inlines = (UserAnswersInline,)


admin.site.register(OriginalString, OriginalAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(UserAnswers, UserAnswersAdmin)
admin.site.register(FirstBatch, FBAdmin)
