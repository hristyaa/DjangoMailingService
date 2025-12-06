from .models import AttemptSendMailing
from django.utils import timezone
from django.core.mail import send_mail
from config import settings


class MailingService:

    def send_mailing(self, mailing):
        time_now = timezone.now()


        if mailing.start_time <= time_now < mailing.end_time:

            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                    )

                    AttemptSendMailing.objects.create(
                        attempt_time=timezone.now(),
                        status='successful',
                        server_response='Рассылка успешно отправлена',
                        mailing=mailing,
                        recipient=recipient,
                    )

                except Exception as e:
                    AttemptSendMailing.objects.create(
                        attempt_time=timezone.now(),
                        status='failed',
                        server_response=f'При отправке возникла ошибка {str(e)}',
                        mailing=mailing,
                        recipient=recipient,
                    )
        else:
            print('Рассылка не может быть отправлена, текущее время не находится в диапазоне времени отправки')