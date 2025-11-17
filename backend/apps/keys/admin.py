from django.contrib import admin
from .models import KeyItem, Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(KeyItem)
class KeyItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'username', 'user', 'folder', 'created_at', 'updated_at']
    list_filter = ['user', 'folder', 'created_at']
    search_fields = ['url', 'username', 'user__email', 'tags', 'note']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    raw_id_fields = ['user', 'folder']
    fieldsets = (
        ('Información Principal', {
            'fields': ('id', 'url', 'username', 'encrypted_pass')
        }),
        ('Detalles', {
            'fields': ('note', 'tags')
        }),
        ('Relaciones', {
            'fields': ('user', 'folder')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
