from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'username', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información de Autenticación', {
            'fields': ('id', 'email', 'username', 'password', 'salt')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Metadata', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Crear Usuario', {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'salt', 'is_staff', 'is_superuser'),
        }),
    )
