from django.contrib import admin
from django.utils.html import format_html

class BaseModelAdmin(admin.ModelAdmin):

    readonly_fields = [
        "uid",
        "created_at",
        "updated_at",
        "status",
    ]

    list_per_page = 25
    save_on_top = True
    def get_readonly_fields(self, request, obj=None):

        readonly_fields = list(self.readonly_fields)
        if obj:  # Editing an existing object
            readonly_fields.extend(['uid'])
        return readonly_fields

    def uid_display(self, obj):

        if obj.uid:
            return format_html(
                '<code style="font-size: 11px;">{}</code>',
                str(obj.uid)[:8] + '...'
            )
        return '-'
    uid_display.short_description = 'UID'

    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'ACTIVE': 'green',
            'INACTIVE': 'red',
            'PENDING': 'orange',
            'SUSPENDED': 'purple'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'

    def save_model(self, request, obj, form, change):

        if not change:  # Creating new object
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)

