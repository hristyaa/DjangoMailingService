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

