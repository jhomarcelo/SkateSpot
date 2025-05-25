from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser')
    list_display_links = ('username', 'email')
    list_filter = ('is_active', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_editable = ('is_active',)

    fieldsets = UserAdmin.fieldsets + (
        ('Foto de Perfil', {
            'fields': ('profile_picture',),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Foto de Perfil', {
            'fields': ('profile_picture',),
        }),
    )