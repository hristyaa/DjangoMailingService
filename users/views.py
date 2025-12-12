import secrets

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse

from config import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail

from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView

from users.forms import UserRegisterForm, UserLoginForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject='Подтверждение почты',
            message=f"Здравствуйте, перейдите по ссылки для подтверждения почты {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"


class UserListView(ListView):
    model = User
    context_object_name = 'account_user'
    template_name = 'users/users_list.html'
    permission_required = 'users.can_view_users_list'


class UserDetailView(DetailView):
    model = User
    context_object_name = 'account_user'
    template_name = 'users/user_detail.html'
    permission_required = 'users.can_view_users_list'


@login_required
@permission_required('users.can_block_users', raise_exception=True)
def blocked_users(request, pk):
    """Блокировка пользователя (для менеджера)"""
    user = get_object_or_404(User, pk=pk)
    user.is_blocked = True
    user.save()
    return redirect(reverse('users:detail_user', kwargs={'pk': user.pk}))


@login_required
@permission_required('users.can_unblock_users', raise_exception=True)
def unblocked_users(request, pk):
    """Разблокировка пользователя (для менеджера)"""
    user = get_object_or_404(User, pk=pk)
    user.is_blocked = False
    user.save()
    return redirect(reverse('users:detail_user', kwargs={'pk': user.pk}))


class UserPasswordResetView(PasswordResetView):
    '''Класс позволяет пользователю сбросить пароль, сгенерировав одноразовую ссылку,
    которую можно использовать для сброса пароля,
    и отправив эту ссылку на зарегистрированный адрес электронной почты пользователя.'''
    email_template_name = "users/password_reset_email.html" # письмо, которое придет на почту
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "users/password_reset_form.html"


class UserPasswordResetDoneView(PasswordResetDoneView):
    '''Подтверждение отправки сообщения с инструкцией на почту '''
    template_name = "users/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """Подтверждение cмены пароля"""
    success_url = reverse_lazy("users:password_reset_complete")
    template_name = "users/password_reset_confirm.html"


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """Информация о смене пароля"""
    template_name = "users/password_reset_complete.html"
    success_url = reverse_lazy("users:login")




