from django.forms import ModelForm

from mailing_service.models import *
from django.core.exceptions import ValidationError


class MailingRecipientForm(StyleFormMixin, ModelForm):
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
        exclude = ('created_at', 'status',)

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['launched_at'].widget.attrs.update(
            {
                'class': 'form-control',
                'type': 'date', }
        )

        self.fields['completed_at'].widget.attrs.update(
            {
                'class': 'form-control',
                'type': 'date', }
        )

        self.fields['message'].widget.attrs.update(
            {
                'class': 'form-control', }
        )

        self.fields['recipients'].widget.attrs.update(
            {
                'class': 'form-control', }
        )