from django.contrib import admin

from mailing_service.models import *
# Register your models here.

@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comment')
    search_fields = ('name', 'email', 'comment')
