from django.contrib import admin
from listings.models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'selling_currency', 'buying_currency', 'is_published', 'is_completed')

admin.site.register(Listing, ListingAdmin)