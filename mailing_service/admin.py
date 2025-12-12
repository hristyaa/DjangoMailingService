from django.contrib import admin

from mailing_service.models import (
    AttemptSendMailing,
    Mailing,
    MailingMessage,
    MailingRecipient,
)

# Register your models here.


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "comment")
    search_fields = ("name", "email", "comment")


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "message")
    search_fields = ("subject", "message")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "start_time",
        "end_time",
        "status",
        "message",
        "recipients_count",
        "recipients_list",
    )
    search_fields = ("status", "message")


@admin.register(AttemptSendMailing)
class AttemptSendMailing(admin.ModelAdmin):
    list_display = (
        "id",
        "attempt_time",
        "status",
        "server_response",
        "mailing",
        "recipient",
    )
    search_fields = ("status", "mailing")
