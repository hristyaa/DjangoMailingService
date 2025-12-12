from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команды для создания группы 'Менеджеры' с правами:
    Может просматривать всех клиентов;
    Может просматривать все сообщения;
    Может просматривать все рассылки;
    Может отключать рассылки;
    Может просматривать список пользователей;
    Может блокировать пользователей;
    Может разблокировать пользователей
    и добавления в группу всех пользоватилей с is_staff=True
    """
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")
        if created:
            print("Группа создана")
        else:
            print("Группа уже существует")

        permissions = Permission.objects.filter(
            codename__in=[
                "can_view_all_recipients",
                "can_view_all_messages",
                "can_view_all_mailings",
                "can_disable_mailing",
                "can_view_users_list",
                "can_block_users",
                "can_unblock_users",
            ]
        )

        group.permissions.set(permissions)

        managers = User.objects.filter(is_staff=True)

        for user in managers:
            user.groups.add(group)
