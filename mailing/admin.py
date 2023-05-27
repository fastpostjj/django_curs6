from django.contrib import admin
from mailing.models import Client, UserMessage


# Register your models here.
@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email','comment', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'email','comment', 'is_active')
    search_fields = ('name', 'email','comment', 'is_active')


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'text')
    search_fields = ('title', 'text')
