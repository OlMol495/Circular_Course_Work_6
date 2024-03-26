from django.contrib import admin
from distribution.models import Client, CircularSettings, Message, Logs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comments',)
    search_fields = ('name', 'email',)
    list_filter = ('name', 'email',)


@admin.register(CircularSettings)
class CircularSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'frequency', 'status',)
    search_fields = ('start_time', 'frequency', 'status',)
    list_filter = ('start_time', 'frequency', 'status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message',)
    search_fields = ('title', 'message',)
    list_filter = ('title',)


@admin.register(Logs)
class AdminLog(admin.ModelAdmin):
    list_display = ('date', 'status', 'response', 'circular', 'client')
    search_fields = ('date', 'client',)
    list_filter = ('status',)
