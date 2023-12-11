from django.contrib import admin

from app.models import Customer, FAQ
from core.constants import EMPTY_FIELD_VALUE


class FAQAdmin(admin.ModelAdmin):
    """Админка для часто задаваемых вопросов."""
    empty_value_display = EMPTY_FIELD_VALUE
    list_display = ('pk', 'question', 'order',)
    search_fields = ('question', 'answer',)


class CustomerAdmin(admin.ModelAdmin):
    """Админка для клиентов."""
    empty_value_display = EMPTY_FIELD_VALUE
    list_display = ('pk', 'name', 'email', 'tg_id', 'phone')
    search_fields = ('name', 'tg_id')


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Customer, CustomerAdmin)
