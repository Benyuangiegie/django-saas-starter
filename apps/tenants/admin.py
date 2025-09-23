from django.contrib import admin
from django.utils.html import format_html
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'domain', 'is_active_display', 
        'user_count_display', 'max_users', 'created_at'
    ]
    list_filter = ['is_active', 'created_at', 'max_users']
    search_fields = ['name', 'slug', 'domain', 'contact_email']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'updated_at', 'user_count_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'domain', 'is_active')
        }),
        ('Limits & Settings', {
            'fields': ('max_users',)
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Address', {
            'fields': (
                'address_line1', 'address_line2', 'city', 
                'state', 'postal_code', 'country'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'user_count_display'),
            'classes': ('collapse',)
        })
    )
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    is_active_display.short_description = 'Status'
    
    def user_count_display(self, obj):
        count = obj.user_count
        max_users = obj.max_users
        if count >= max_users:
            color = 'red'
        elif count >= max_users * 0.8:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {};">{}/{}</span>', 
            color, count, max_users
        )
    user_count_display.short_description = 'Users'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()