from django.db import models


# Create your models here.

class MailingRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    name = models.CharField(max_length=250, verbose_name="Ф.И.О.")
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
    launched_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=12, choices=MAILING_STATUS, default=CREATED, verbose_name='Статус рассылки')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='Сообщение')
    recipients = models.ManyToManyField(MailingRecipient, blank=True, verbose_name='Получатели')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания рассылки')

    def __str__(self):
        return f'Рассылка создана {self.created_at}, статус: {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = [
            'status',
        ]
