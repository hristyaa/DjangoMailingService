from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from config.settings import CACHE_ENABLED

from .models import AttemptSendMailing, Mailing, MailingMessage, MailingRecipient


class MailingService:

    def send_mailing(self, mailing):
        time_now = timezone.now()

        if mailing.start_time <= time_now < mailing.end_time:

            for recipient in mailing.recipients.all():
                try:
                    self.validate_email(recipient.email)

                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                    )

                    AttemptSendMailing.objects.create(
                        attempt_time=timezone.now(),
                        status="successful",
                        server_response="Рассылка успешно отправлена",
                        mailing=mailing,
                        recipient=recipient,
                    )

                except ValidationError as ve:
                    AttemptSendMailing.objects.create(
                        attempt_time=timezone.now(),
                        status="failed",
                        server_response=f"При отправке возникла ошибка {str(ve)}",
                        mailing=mailing,
                        recipient=recipient,
                    )

                except Exception as e:
                    AttemptSendMailing.objects.create(
                        attempt_time=timezone.now(),
                        status="failed",
                        server_response=f"При отправке возникла ошибка {str(e)}",
                        mailing=mailing,
                        recipient=recipient,
                    )
        else:
            print(
                "Рассылка не может быть отправлена, текущее время не находится в диапазоне времени отправки"
            )

    def validate_email(self, email):
        if not (
            email.endswith("@gmail.com")
            or email.endswith("@yandex.ru")
            or email.endswith("@mail.ru")
        ):
            raise ValidationError("Неверный формат email")


def get_recipient_from_cache():
    """Получение клиентов (получателей рассылки) из кэша, если кэш пуст, получаем данные из бд"""
    if not CACHE_ENABLED:
        return MailingRecipient.objects.all()
    recipients = cache.get("recipients_list")
    if recipients is not None:
        return recipients
    recipients = MailingRecipient.objects.all()
    cache.set("recipients_list", recipients)
    return recipients


def get_messages_from_cache():
    """Получение сообщений из кэша, если кэш пуст, получаем данные из бд"""
    if not CACHE_ENABLED:
        return MailingMessage.objects.all()
    messages = cache.get("messages_list")
    if messages is not None:
        return messages
    messages = MailingMessage.objects.all()
    cache.set("messages_list", messages)
    return messages


def get_mailing_from_cache():
    """Получение рассылки из кэша, если кэш пуст, получаем данные из бд"""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    mailings = cache.get("mailings_list")
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set("mailings_list", mailings)
    return mailings
