from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing_service.models import MailingRecipient


class HomePageView(TemplateView):
    template_name = 'mailing_service/home.html'


class MailingRecipientListView(ListView):
    model = MailingRecipient
    context_object_name = 'clients'
    template_name = 'mailing_service/mailing_recipient_list.html'


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    fields = ['name', 'email', 'comment']
    context_object_name = 'client'
    template_name = 'mailing_service/mailing_recipient_form.html'
    success_url = reverse_lazy('mailing_service:clients')
