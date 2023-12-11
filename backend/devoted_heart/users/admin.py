from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User
from core.constants import EMPTY_FIELD_VALUE


class UserAdmin(admin.ModelAdmin):
    empty_value_display = EMPTY_FIELD_VALUE
    """Админка для пользователя."""
    list_display = (
        'username',
        'email',
        'name',
        'surname',
        'tg_id',
    )
    list_filter = ('username',)
    search_fields = ('username', 'surname', 'tg_id')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
