from django.contrib import admin
from listings.models import Listing, ServiceFee


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'selling_currency', 'buying_currency', 'is_published', 'is_completed')
    readonly_fields = ['created', 'updated', 'service_rate']

    # def has_change_permission(self, request, obj=None):
    #     return False

class ServiceFeeAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Listing, ListingAdmin)
admin.site.register(ServiceFee, ServiceFeeAdmin)
