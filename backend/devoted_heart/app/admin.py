import logging
from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from django_object_actions import DjangoObjectActions
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from rangefilter.filters import DateRangeFilterBuilder

from app.forms import MessagesForm
from app.models import Customer, FAQ, Messages, Category, SchedulerSettings
from core.constants import EMPTY_FIELD_VALUE
from app.regular_messages import send_messages, start_scheduler, stop_scheduler

logger = logging.getLogger(__name__)


class CategoryAdmin(admin.ModelAdmin):
    """Админка модели Категории."""
    list_display = ('pk', 'name',)
    list_display_links = ('name',)


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
    list_filter = ('category', )


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


class MessagesAdmin(DjangoObjectActions, admin.ModelAdmin):
    """
    Админка для сообщений: админ может добавить текстовое сообщение
    дополнительно к рассылаемым random сообщениям из regular_messages.
    Например: Привет от Фуражкина!!!
    """
    list_display = ('text', 'display_image', 'selected',)
    form = MessagesForm
    list_editable = ('selected',)
    actions = [
        'send_messages_view',
        'start_scheduler',
        'stop_scheduler'
    ]

    changelist_actions = ('start_scheduler', 'stop_scheduler')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'send_messages/', self.send_messages_view, name='send_messages'
            ),
            path(
                'start_scheduler/', self.start_scheduler,
                name='start_scheduler'
            ),
            path(
                'stop_scheduler/', self.stop_scheduler, name='stop_scheduler'
                ),
        ]
        return custom_urls + urls

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px; width: auto"/>',
                obj.image.url
            )
        return 'Отсутствует'
    display_image.short_description = 'Фото'
    # display_image.allow_tags = True
    display_image.admin_order_field = 'image'

    def send_messages_view(self, request, queryset=None):
        """Отправка одного сообщения"""
        selected_messages = (
            list(queryset) if queryset else Messages.objects.filter(
                selected=True
            )
        )
        if not selected_messages:
            self.message_user(
                request, (
                    'Не выбрано сообщение. '
                    'Выберите хотя бы одно сообщение - '
                    'через чекбокс "добавить к планировщику"'
                )
            )
            return render(request, 'admin/send_messages_done.html')
        try:
            send_messages(selected_messages)
            self.message_user(
                request,
                'Сообщения успешно отправлены подписчикам.'
            )
        except Exception as e:
            logger.error(f"Ошибка отправки сообщений: {e}")
            self.message_user(
                request,
                'Произошла ошибка при отправке сообщений.'
            )
        return render(request, 'admin/send_messages_done.html')
    send_messages_view.short_description = "Отправить сообщение"

    def start_scheduler(self, request, queryset=None):
        """Планировщик заданий - рассылка регулярных сообщений"""
        try:
            start_scheduler()
            self.message_user(request, 'Планировщик успешно запущен.')
        except Exception as e:
            logger.error(f"Ошибка при запуске планировщика: {e}")
            self.message_user(
                request,
                'Ошибка при запуске планировщика.'
            )
        return render(request, 'admin/start_scheduler_done.html')
    start_scheduler.short_description = "Запустить планировщик"
    start_scheduler.label = 'Запустить планировщик'

    def stop_scheduler(self, request, queryset=None):
        """Планировщик заданий - остановка рассылки регулярных сообщений"""
        try:
            stop_scheduler()
            self.message_user(request, 'Планировщик успешно остановлен.')
        except Exception as e:
            logger.error(f"Ошибка при остановке планировщика: {e}")
            self.message_user(
                request,
                'Ошибка при остановке планировщика.'
            )
        return render(request, 'admin/stop_scheduler_done.html')
    stop_scheduler.short_description = "Остановить планировщик"
    stop_scheduler.label = 'Остановить планировщик'


class SchedulerSettingsAdmin(admin.ModelAdmin):
    """Админка для планирования рассылки"""
    list_display = ('scheduler_period', )

    def has_add_permission(self, request):
        """
        Проверка на наличие записи перед разрешением добавления новой записи.
        Страховка. Может быть только одна запись.
        """
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        """Запрет удаления записи. Страховка"""
        return False


delete_selected.short_description = 'Удалить выбранное'


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Messages, MessagesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SchedulerSettings, SchedulerSettingsAdmin)

admin.site.site_header = 'Преданное сердце'
admin.site.site_title = 'Преданное сердце'
admin.site.index_title = 'Управление'
