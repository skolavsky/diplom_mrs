from django.contrib import admin
from .models import SupportTicket

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'message', 'status', 'created_at', 'admin_response')
    search_fields = ('user__username', 'email', 'message')
    list_filter = ('status', 'created_at')

admin.site.register(SupportTicket, SupportTicketAdmin)
