from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"

@register.filter(name='in_group')
def in_group(user, group_name):
    """Проверяет, состоит ли пользователь в указанной группе"""
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False
