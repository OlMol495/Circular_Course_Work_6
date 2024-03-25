from django.contrib import admin
from users.models import User

admin.site.register(User)

# @admin.register(User)
# class AdminUser(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar',
#                     'email_confirmed', 'is_active', 'is_staff', 'is_superuser')
#     search_fields = ('email', 'first_name', 'last_name', 'telegram')
#     list_filter = ('email_confirmed', 'is_active', 'is_staff')
