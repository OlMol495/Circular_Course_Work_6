from django.contrib import admin
from distribution.models import Client, CircularSettings, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comments',)
    search_fields = ('name', 'email',)
    list_filter = ('name', 'email',)


@admin.register(CircularSettings)
class CircularSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'frequency', 'status',)
    search_fields = ('start_date', 'frequency', 'status',)
    list_filter = ('start_date', 'frequency', 'status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message',)
    search_fields = ('title', 'message',)
    list_filter = ('title',)

