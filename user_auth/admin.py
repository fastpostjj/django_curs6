from django.contrib import admin

from user_auth.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    email
    phone
    is_blocked
    """
    list_display = ('id', 'email', 'phone', 'first_name', 'last_name', 'country', 'is_blocked')

    list_filter = ('id', 'email', 'phone', 'first_name', 'last_name', 'country', 'is_blocked')
    list_display_links = ('id', 'email', 'phone', 'first_name', 'last_name', 'country', 'is_blocked')
