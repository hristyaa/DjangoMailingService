# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing_service.forms import MailingForm, MailingRecipientForm, MailingMessageForm
from mailing_service.models import Mailing, MailingMessage, MailingRecipient, AttemptSendMailing
from mailing_service.services import MailingService


class HomePageView(TemplateView):
    template_name = 'mailing_service/home.html'

    def get_context_data(self, **kwargs):
        total_mailings = Mailing.objects.count()  # Всего рассылок
        active_mailings = Mailing.objects.filter(status='launched').count()  # Кол-во активных рассылок
        unique_recipients = MailingRecipient.objects.distinct().count()  # Уникальные получатели

        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
        }
        return context


class MailingRecipientListView(ListView):
    model = MailingRecipient
    context_object_name = 'clients'
    template_name = 'mailing_service/mailing_recipient_list.html'


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    context_object_name = 'client'
    template_name = 'mailing_service/mailing_recipient_form.html'
    success_url = reverse_lazy('mailing_service:clients')


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    context_object_name = 'client'
    template_name = 'mailing_service/mailing_recipient_detail.html'


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    context_object_name = 'client'
    template_name = 'mailing_service/mailing_recipient_form.html'
    success_url = reverse_lazy('mailing_service:clients')

    def get_success_url(self):
        return reverse('mailing_service:detail_client', args=[self.kwargs.get('pk')])


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    context_object_name = 'client'
    template_name = 'mailing_service/mailing_recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:clients')


class MailingMessageListView(ListView):
    model = MailingMessage
    context_object_name = 'messages'
    template_name = 'mailing_service/messages_list.html'


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    context_object_name = 'message'
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('mailing_service:messages')


class MailingMessageDetailView(DetailView):
    model = MailingMessage
    context_object_name = 'message'
    template_name = 'mailing_service/message_detail.html'


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    context_object_name = 'message'
    template_name = 'mailing_service/message_form.html'
    success_url = reverse_lazy('mailing_service:messages')

    def get_success_url(self):
        return reverse('mailing_service:detail_message', args=[self.kwargs.get('pk')])


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    context_object_name = 'message'
    template_name = 'mailing_service/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:messages')


class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailing_service/mailing_list.html'

    def get_queryset(self):
        mailings = super().get_queryset()

        # Обновляем статусы для всех рассылок
        for mailing in mailings:
            mailing.update_status()

        return mailings


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    context_object_name = 'mailing'
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailings')


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing_service/mailing_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status() # ← пересчёт и сохранение статуса
        return obj


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    context_object_name = 'mailing'
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailings')

    def get_success_url(self):
        return reverse('mailing_service:detail_mailing', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing_service/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:mailings')


class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        service = MailingService()
        service.send_mailing(mailing)
        mailing.update_status()
        return redirect('mailing_service:detail_mailing', pk=pk)

def mailing_report(request):
    # Получаем все попытки, сортируя по времени
    attempts = AttemptSendMailing.objects.order_by('-attempt_time')

    # Считаем успешные и неуспешные попытки
    success_count = AttemptSendMailing.objects.filter(status=AttemptSendMailing.SUCCESSFUL).count()
    failed_count = AttemptSendMailing.objects.filter(status=AttemptSendMailing.FAILED).count()

    # Общее количество отправленных сообщений
    total_messages = attempts.count()

    # Передаем данные в шаблон
    context = {
        'attempts': attempts,
        'success_count': success_count,
        'failed_count': failed_count,
        'total_messages': total_messages,
    }
    return render(request, 'mailing_service/attempt_send_mailing.html', context)
