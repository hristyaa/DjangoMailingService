from django.db import models
from django.utils import timezone

# Create your models here.


class MailingRecipient(models.Model):
    name = models.CharField(max_length=250, verbose_name="Ф.И.О.")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = "получатель рассылки"
        verbose_name_plural = "получатели рассылки"
        ordering = [
            "name",
        ]


class MailingMessage(models.Model):
    subject = models.CharField(max_length=250, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Письмо")

    def __str__(self):
        return f'{self.subject} - {self.message}'

    class Meta:
        verbose_name = "Cooбщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "subject",
        ]


class Mailing(models.Model):
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'

    MAILING_STATUS = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]
    start_time = models.DateTimeField(verbose_name='Дата и время начала отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=12, choices=MAILING_STATUS, default=CREATED, verbose_name='Статус рассылки')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Сообщение')
    recipients = models.ManyToManyField(MailingRecipient, blank=True, verbose_name='Получатели')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания рассылки')

    def update_status(self):
        '''Метод для определения статуса рассылки на основе текущего времени'''
        time_now = timezone.now()
        new_status = self.status

        if time_now < self.start_time:
            new_status = self.CREATED

        elif time_now >= self.end_time:
            new_status = self.COMPLETED

        elif self.start_time <= time_now < self.end_time:
            new_status = self.LAUNCHED

        if self.status != new_status:
            self.status = new_status
            self.save()

        return new_status

    def __str__(self):
        return f'Рассылка создана {self.created_at}, статус: {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = [
            'status',
        ]

    def recipients_list(self):
        """Возвращает строку с получателями для админки"""
        return ", ".join([str(recipient) for recipient in self.recipients.all()[:3]])

    recipients_list.short_description = 'Получатели'

    def recipients_count(self):
        """Возвращает количество получателей"""
        return self.recipients.count()

    recipients_count.short_description = 'Кол-во получателей'


class AttemptSendMailing(models.Model):
    SUCCESSFUL = 'successful'
    FAILED = 'failed'

    SEND_MAILING_STATUS = [
        (SUCCESSFUL, 'Успешно'),
        (FAILED, 'Не успешно'),
    ]
    attempt_time = models.DateTimeField(verbose_name='Дата и время начала попытки рассылки')
    status = models.CharField(max_length=12, choices=SEND_MAILING_STATUS, verbose_name='Статус попытки рассылки')
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    recipient = models.ForeignKey(MailingRecipient, on_delete=models.CASCADE, verbose_name='Получатель' )

    def __str__(self):
        return f'{self.mailing}, {self.recipient}: {self.status} - {self.server_response}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылок'
        ordering = [
            'status',
        ]
