from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# class UserAdmin(admin.ModelAdmin):
#     pass
    # def __init__(self):
    #     super(UserAdmin, self).__init__()
#     pass
    # class Meta:
    #     model = User
    #     fields = "__all__"
    # list_display = [field.name for field in User._meta.fields if field.name != "id"]


    # fieldsets = (
    #         (None, {"fields": ("email", "username", "password")}),
    #         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    #     )
    #
    # readonly_fields = ["password"]
UserAdmin.fieldsets = (
            (None, {"fields": ("uuid", "username", "password")}),
            ("Personal info", {"fields": ("first_name", "last_name")}),
            ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
            ("Important dates", {"fields": ("last_login", "date_joined")}),
)

UserAdmin.readonly_fields = ["uuid"]

UserAdmin.search_fields = ['username', 'first_name', 'last_name', 'uuid']

# UserAdmin.ordering = ('email',)

admin.site.register(User, UserAdmin)
