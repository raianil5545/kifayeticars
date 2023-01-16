from django.contrib import admin

from .models import AppUser


@admin.register(AppUser)
class UserAdminModel(admin.ModelAdmin):
    search_fields = ("first_name", "email", )
    list_filter = ("email", "first_name", "is_active", "date_joined", )
    ordering = ("-date_joined", )
    list_display = ("email", "first_name", "is_active", "is_staff", )
    add_fieldsets = (
        (None, {
            "classes": ("wide", ),
            "fields": ("email", "first_name",
                       "last_name", "password1", "password2",)
        }),
    )
