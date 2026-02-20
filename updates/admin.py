"""
Admin configuration for updates app.
"""
from django.contrib import admin
from .models import Update


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing updates and news.
    """
    list_display = [
        'title',
        'update_type',
        'published_at',
        'is_featured',
        'is_published',
        'source',
    ]
    
    list_filter = [
        'update_type',
        'is_published',
        'is_featured',
        'published_at',
    ]
    
    search_fields = [
        'title',
        'content',
        'source',
    ]
    
    readonly_fields = [
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'update_type')
        }),
        ('Related Content', {
            'fields': ('related_outbreak',)
        }),
        ('Media', {
            'fields': ('image', 'document')
        }),
        ('Publishing', {
            'fields': ('published_at', 'updated_at', 'source', 'is_published', 'is_featured')
        }),
    )
    
    date_hierarchy = 'published_at'
    
    actions = ['mark_as_featured', 'mark_as_published']
    
    def mark_as_featured(self, request, queryset):
        """Mark selected updates as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} update(s) marked as featured.')
    mark_as_featured.short_description = "Mark selected updates as featured"
    
    def mark_as_published(self, request, queryset):
        """Mark selected updates as published."""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} update(s) published.')
    mark_as_published.short_description = "Publish selected updates"