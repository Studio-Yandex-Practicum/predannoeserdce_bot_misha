from datetime import datetime

from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilterBuilder

from app.models import Customer, FAQ
from core.constants import EMPTY_FIELD_VALUE


class FAQResource(resources.ModelResource):
    class Meta:
        model = FAQ


class FAQAdmin(ImportExportActionModelAdmin):
    """Админка модели Часто задаваемые вопросы"""
    resource_class = FAQResource
    empty_value_display = EMPTY_FIELD_VALUE
    list_display = ('pk', 'question', 'answer', 'category', 'order',)
    list_display_links = ('question',)
    search_fields = ('question', 'order', 'category')
    list_editable = ('order', )


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


class CustomerAdmin(ImportExportActionModelAdmin):
    """Админка модели Клиент"""
    resource_class = CustomerResource
    list_display = (
        'pk', 'name', 'email', 'tg_id', 'phone', 'registration_date'
    )
    list_display_links = ('name',)
    search_fields = ('name__startswith', 'email__startswith', 'phone')
    list_filter = (
        ('registration_date', DateRangeFilterBuilder()),
    )


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Customer, CustomerAdmin)
