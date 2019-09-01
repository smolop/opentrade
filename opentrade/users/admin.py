from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from opentrade.users.models import User, Profile

class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'is_verified','is_staff')
    list_filter = ('is_staff', 'created', 'modified', 'is_verified')


admin.site.register(Profile)

admin.site.register(User, CustomUserAdmin)