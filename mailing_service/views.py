from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing_service.models import MailingRecipient


class MailingRecipientListView(ListView):
    model = MailingRecipient
    context_object_name = 'client'
    template_name = 'mailing_service/base.html'

