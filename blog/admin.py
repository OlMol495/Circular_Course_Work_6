from django.contrib import admin
from blog.models import Post



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'text', 'is_published', 'preview_image', 'created', 'views',)
    list_filter = ('title', 'is_published', 'created', 'updated')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
