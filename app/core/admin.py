"""Django admin customnizastion"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _  #if you need to translate app in future

from core import models

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user"""
    ordering = ['id']
    list_display=['email', 'name']
    fieldsets=(  #Modified fieldset that contain the fields that we have in our models
        (None, {'fields':('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'),{'fields': ('last_login',)}),
    )
    readonly_fields=['last_login']
    add_fieldsets=(
        (None, {
            'classes':('wide',), #css class
            'fields':(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',

            )
        }),
    )

admin.site.register(models.User, UserAdmin)