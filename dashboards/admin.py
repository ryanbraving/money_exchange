from django.contrib import admin
from .models import Dashboard

class DashboardAdmin(admin.ModelAdmin):
    list_display = ('id',)
    # list_display = ('id', 'requester_name', 'listing', 'requester_email', 'grabbed_on')
    # list_display_links = ('id', 'requester_name')
    # search_fields = ('requester_name', 'requester_email', 'listing')
    list_per_page = 50

admin.site.register(Dashboard, DashboardAdmin)