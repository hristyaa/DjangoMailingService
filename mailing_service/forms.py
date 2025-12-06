from django.forms import ModelForm
from django import forms
from mailing_service.models import Mailing, MailingMessage, MailingRecipient
from django.core.exceptions import ValidationError
from django.utils import timezone


class MailingRecipientForm(ModelForm):
    class Meta:
        model = MailingRecipient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MailingRecipientForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите имя получателя', }
        )

        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите email получателя', }
        )

        self.fields['comment'].widget.attrs.update(
            {
                'class': 'form-control',
            }
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (email.endswith('@gmail.com') or
        email.endswith('@yandex.ru') or
        email.endswith('@mail.ru')):
            raise ValidationError('Email должен оканчиваться на @gmail.com, @yandex.ru или @mail.ru')
        return email


class MailingMessageForm(ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MailingMessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите тему письма', }
        )

        self.fields['message'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите текст письма', }
        )


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        exclude = ('created_at', 'status', 'is_sent')
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Select(attrs={'class': 'form-select', 'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['start_time'].required = True
        self.fields['end_time'].required = True

        self.fields['start_time'].widget.attrs.update(
            {
                'class': 'form-control',
                'type': 'datetime-local', }
        )

        self.fields['end_time'].widget.attrs.update(
            {
                'class': 'form-control',
                'type': 'datetime-local', }
        )

        self.fields['message'].widget.attrs.update(
            {
                'class': 'form-control',
                'size': '5', }
        )

        self.fields['recipients'].widget.attrs.update(
            {
                'class': 'form-control', }

        )

    def clean_start_time(self):
        """Валидация даты и времени начала отправки (не может быть в прошлом, раньше end_time)"""
        start_time = self.cleaned_data.get('start_time')
        time_now = timezone.now()

        if not start_time:
            raise ValidationError('Укажите дату и время начала отправки')

        if start_time:
            if start_time < time_now:
                raise ValidationError('Дата и время начала отправки не может быть в прошлом')
        return start_time

    def clean_end_time(self):
        """Валидация даты и времени начала отправки (не может быть в прошлом, раньше end_time)"""
        end_time = self.cleaned_data.get('end_time')
        time_now = timezone.now()

        if not end_time:
            raise ValidationError('Укажите дату и время окончания отправки')

        if end_time < time_now:
            raise ValidationError('Дата и время окончания отправки не может быть в прошлом')
        return end_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                self.add_error(
                    'start_time',
                    'Дата и время начала отправки не может быть позже даты и времени окончания отправки'
                )
