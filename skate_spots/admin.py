from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_superuser')
    list_display_links = ('username', 'email')
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'user_type')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_editable = ('is_active',)

    fieldsets = UserAdmin.fieldsets + (
        ('Foto de Perfil', {
            'fields': ('profile_picture','user_type'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Foto de Perfil', {
            'fields': ('profile_picture','user_type'),
        }),
    )