# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing_service.forms import MailingForm, MailingMessageForm, MailingRecipientForm
from mailing_service.models import (
    AttemptSendMailing,
    Mailing,
    MailingMessage,
    MailingRecipient,
)
from mailing_service.services import (
    MailingService,
    get_mailing_from_cache,
    get_messages_from_cache,
    get_recipient_from_cache,
)


class HomePageView(TemplateView):
    template_name = "mailing_service/home.html"

    def get_context_data(self, **kwargs):
        total_mailings = Mailing.objects.count()  # Всего рассылок
        active_mailings = Mailing.objects.filter(
            status="launched"
        ).count()  # Кол-во активных рассылок
        unique_recipients = (
            MailingRecipient.objects.distinct().count()
        )  # Уникальные получатели

        context = {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_recipients": unique_recipients,
        }
        return context


class MailingRecipientListView(ListView):
    model = MailingRecipient
    context_object_name = "clients"
    template_name = "mailing_service/mailing_recipient_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "mailing_service.can_view_all_recipients"
        ):
            return MailingRecipient.objects.all()
        elif self.request.user.is_authenticated:
            return MailingRecipient.objects.filter(owner=self.request.user)


class MailingRecipientCreateView(CreateView, LoginRequiredMixin):
    model = MailingRecipient
    form_class = MailingRecipientForm
    context_object_name = "client"
    template_name = "mailing_service/mailing_recipient_form.html"
    success_url = reverse_lazy("mailing_service:clients")

    def form_valid(self, form):
        """Фиксация владельца при создании"""
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    context_object_name = "client"
    template_name = "mailing_service/mailing_recipient_detail.html"

    def get_queryset(self):
        return get_recipient_from_cache()


class MailingRecipientUpdateView(UpdateView, LoginRequiredMixin):
    model = MailingRecipient
    form_class = MailingRecipientForm
    context_object_name = "client"
    template_name = "mailing_service/mailing_recipient_form.html"
    success_url = reverse_lazy("mailing_service:clients")

    def get_success_url(self):
        return reverse("mailing_service:detail_client", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        """Получение доступа к форме"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingRecipientForm
        raise PermissionDenied


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    context_object_name = "client"
    template_name = "mailing_service/mailing_recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing_service:clients")


class MailingMessageListView(ListView):
    model = MailingMessage
    context_object_name = "messages"
    template_name = "mailing_service/messages_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm(
            "mailing_service.can_view_all_messages"
        ):
            return MailingMessage.objects.all()
        elif self.request.user.is_authenticated:
            return MailingMessage.objects.filter(owner=self.request.user)


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    context_object_name = "message"
    template_name = "mailing_service/message_form.html"
    success_url = reverse_lazy("mailing_service:messages")

    def form_valid(self, form):
        """Фиксация владельца при создании"""
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MailingMessageDetailView(DetailView):
    model = MailingMessage
    context_object_name = "message"
    template_name = "mailing_service/message_detail.html"

    def get_queryset(self):
        return get_messages_from_cache()


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    context_object_name = "message"
    template_name = "mailing_service/message_form.html"
    success_url = reverse_lazy("mailing_service:messages")

    def get_success_url(self):
        return reverse("mailing_service:detail_message", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        """Получение доступа к форме"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingMessageForm
        raise PermissionDenied


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    context_object_name = "message"
    template_name = "mailing_service/message_confirm_delete.html"
    success_url = reverse_lazy("mailing_service:messages")


class MailingListView(ListView):
    model = Mailing
    context_object_name = "mailings"
    template_name = "mailing_service/mailing_list.html"

    def get_queryset(self):
        mailings = super().get_queryset()

        # Обновляем статусы для всех рассылок
        for mailing in mailings:
            mailing.update_status()

        if self.request.user.is_superuser or self.request.user.has_perm(
            "mailing_service.can_view_all_mailings"
        ):
            return mailings
        elif self.request.user.is_authenticated:
            return mailings.filter(owner=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    context_object_name = "mailing"
    template_name = "mailing_service/mailing_form.html"
    success_url = reverse_lazy("mailing_service:mailings")

    def get_form_kwargs(self):
        """Передача текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Фиксация владельца при создании"""
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailing_service/mailing_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.status != Mailing.COMPLETED:
            obj.update_status()  # ← пересчёт и сохранение статуса
        return obj

    def get_queryset(self):
        return get_mailing_from_cache()


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    context_object_name = "mailing"
    template_name = "mailing_service/mailing_form.html"
    success_url = reverse_lazy("mailing_service:mailings")

    def get_success_url(self):
        return reverse("mailing_service:detail_mailing", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        """Получение доступа к форме"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        raise PermissionDenied

    def get_form_kwargs(self):
        """Передача текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(DeleteView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailing_service/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing_service:mailings")


class MailingSendView(View):
    """Отправка рассылки"""

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        service = MailingService()
        service.send_mailing(mailing)
        mailing.update_status()
        return redirect("mailing_service:detail_mailing", pk=pk)


def mailing_report(request):
    # Получаем все  попытки текущего пользователя, сортируя по времени
    if request.user.is_superuser or request.user.has_perm(
        "mailing_service.can_view_all_mailings"
    ):
        attempts = AttemptSendMailing.objects.order_by("-attempt_time")
        success_count = AttemptSendMailing.objects.filter(
            status=AttemptSendMailing.SUCCESSFUL
        ).count()
        failed_count = AttemptSendMailing.objects.filter(
            status=AttemptSendMailing.FAILED
        ).count()
    else:
        attempts = AttemptSendMailing.objects.filter(
            mailing__owner=request.user
        ).order_by("-attempt_time")

        # Считаем успешные и неуспешные попытки текущего пользователя
        success_count = AttemptSendMailing.objects.filter(
            mailing__owner=request.user, status=AttemptSendMailing.SUCCESSFUL
        ).count()
        failed_count = AttemptSendMailing.objects.filter(
            mailing__owner=request.user, status=AttemptSendMailing.FAILED
        ).count()

    # Общее количество отправленных сообщений
    total_messages = attempts.count()

    # Передаем данные в шаблон
    context = {
        "attempts": attempts,
        "success_count": success_count,
        "failed_count": failed_count,
        "total_messages": total_messages,
    }
    return render(request, "mailing_service/attempt_send_mailing.html", context)


def disable_mailing(request, pk):
    """Отключение рассылки - перевод из статуса 'запущена' в 'завершена' (для менеджеров)"""
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = "completed"
    mailing.save()
    return redirect("mailing_service:detail_mailing", pk=mailing.pk)
