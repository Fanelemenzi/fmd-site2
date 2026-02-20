"""
Admin configuration for outbreaks app.
"""
from django.contrib import admin
from .models import Outbreak, DipTank, CordonLine, FootWashStation


@admin.register(Outbreak)
class OutbreakAdmin(admin.ModelAdmin):
    """
    Admin interface for managing outbreaks.
    """
    list_display = [
        'title',
        'status',
        'region',
        'location_name',
        'animals_affected',
        'date_reported',
        'is_verified',
        'is_active',
    ]
    
    list_filter = [
        'status',
        'region',
        'is_verified',
        'is_active',
        'date_reported',
    ]
    
    search_fields = [
        'title',
        'description',
        'location_name',
    ]
    
    readonly_fields = [
        'last_updated',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status', 'region')
        }),
        ('Location', {
            'fields': ('location_name', 'latitude', 'longitude')
        }),
        ('Outbreak Details', {
            'fields': ('animals_affected', 'animals_quarantined')
        }),
        ('Dates', {
            'fields': ('date_reported', 'date_confirmed', 'date_cleared', 'last_updated')
        }),
        ('Source & Verification', {
            'fields': ('source', 'is_verified', 'is_active')
        }),
    )
    
    date_hierarchy = 'date_reported'
    
    actions = ['mark_as_verified', 'mark_as_cleared']
    
    def mark_as_verified(self, request, queryset):
        """Mark selected outbreaks as verified."""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} outbreak(s) marked as verified.')
    mark_as_verified.short_description = "Mark selected outbreaks as verified"
    
    def mark_as_cleared(self, request, queryset):
        """Mark selected outbreaks as cleared."""
        from django.utils import timezone
        updated = queryset.update(status='cleared', date_cleared=timezone.now())
        self.message_user(request, f'{updated} outbreak(s) marked as cleared.')
    mark_as_cleared.short_description = "Mark selected outbreaks as cleared"


@admin.register(DipTank)
class DipTankAdmin(admin.ModelAdmin):
    """
    Admin interface for managing dip tanks.
    """
    list_display = [
        'name',
        'region',
        'is_affected',
        'capacity',
        'last_inspection',
        'is_active',
    ]
    
    list_filter = [
        'region',
        'is_affected',
        'is_active',
        'last_inspection',
    ]
    
    search_fields = [
        'name',
        'notes',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'region', 'is_affected')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('capacity', 'last_inspection', 'notes')
        }),
        ('System', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_affected', 'mark_as_clear', 'mark_as_active']
    
    def mark_as_affected(self, request, queryset):
        """Mark selected dip tanks as affected."""
        updated = queryset.update(is_affected=True)
        self.message_user(request, f'{updated} dip tank(s) marked as affected.')
    mark_as_affected.short_description = "Mark selected dip tanks as affected"
    
    def mark_as_clear(self, request, queryset):
        """Mark selected dip tanks as clear."""
        updated = queryset.update(is_affected=False)
        self.message_user(request, f'{updated} dip tank(s) marked as clear.')
    mark_as_clear.short_description = "Mark selected dip tanks as clear"
    
    def mark_as_active(self, request, queryset):
        """Mark selected dip tanks as active."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} dip tank(s) marked as active.')
    mark_as_active.short_description = "Mark selected dip tanks as active"

@admin.register(CordonLine)
class CordonLineAdmin(admin.ModelAdmin):
    """
    Admin interface for managing cordon lines.
    """
    list_display = [
        'name',
        'region',
        'status',
        'date_established',
        'date_expires',
        'is_active',
    ]
    
    list_filter = [
        'region',
        'status',
        'is_active',
        'date_established',
    ]
    
    search_fields = [
        'name',
        'description',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'region', 'status')
        }),
        ('Line Coordinates', {
            'fields': ('coordinates',),
            'description': 'JSON format: [{"lat": -26.123, "lng": 31.456}, {"lat": -26.124, "lng": 31.457}]'
        }),
        ('Details', {
            'fields': ('description', 'restrictions')
        }),
        ('Dates', {
            'fields': ('date_established', 'date_expires')
        }),
        ('System', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_active', 'mark_as_inactive']
    
    def mark_as_active(self, request, queryset):
        """Mark selected cordon lines as active."""
        updated = queryset.update(status='active', is_active=True)
        self.message_user(request, f'{updated} cordon line(s) marked as active.')
    mark_as_active.short_description = "Mark selected cordon lines as active"
    
    def mark_as_inactive(self, request, queryset):
        """Mark selected cordon lines as inactive."""
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} cordon line(s) marked as inactive.')
    mark_as_inactive.short_description = "Mark selected cordon lines as inactive"


@admin.register(FootWashStation)
class FootWashStationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing foot wash stations.
    """
    list_display = [
        'name',
        'road_name',
        'region',
        'road_type',
        'is_operational',
        'last_maintenance',
        'is_active',
    ]
    
    list_filter = [
        'region',
        'road_type',
        'is_operational',
        'is_active',
        'last_maintenance',
    ]
    
    search_fields = [
        'name',
        'road_name',
        'instructions',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'region', 'road_name', 'road_type')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Instructions & Contact', {
            'fields': ('instructions', 'operating_hours', 'contact_person', 'contact_phone')
        }),
        ('Status', {
            'fields': ('is_operational', 'last_maintenance')
        }),
        ('System', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_operational', 'mark_as_non_operational']
    
    def mark_as_operational(self, request, queryset):
        """Mark selected stations as operational."""
        updated = queryset.update(is_operational=True)
        self.message_user(request, f'{updated} station(s) marked as operational.')
    mark_as_operational.short_description = "Mark selected stations as operational"
    
    def mark_as_non_operational(self, request, queryset):
        """Mark selected stations as non-operational."""
        updated = queryset.update(is_operational=False)
        self.message_user(request, f'{updated} station(s) marked as non-operational.')
    mark_as_non_operational.short_description = "Mark selected stations as non-operational"