from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Acl

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'email', 'photo', 'password')}),
        (_('Personal info'), {'fields': ('name', 'date_of_birth', 'sex')}),
        (_('Permissions'), {'fields': ('is_active', 'is_customer', 'is_vendor', 'is_staff', 'is_superuser',
                                       'acl', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'photo', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'name', 'acl', 'is_staff', 'is_customer', 'is_vendor',)
    list_filter = ('is_staff', 'is_customer', 'is_vendor',)
    search_fields = ('username','email', 'name',)
    ordering = ('username',)

admin.site.register(Acl)