from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from customer.forms import UserModelForm
from customer.models import Customer, User


# Register your models here.
# admin.site.register(Customer)


@admin.register(Customer)
class CustomerModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'is_active']
    search_fields = ['email', 'id']
    list_filter = ['joined', 'is_active']
    def save_model(self, request, obj, form, change):
        # Ensure any custom logic or save operations handle field types correctly
        obj.save()

    def has_add_permission(self, request):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(User)
class UserModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['email', 'username', 'birth_of_date', 'is_superuser']
    form = UserModelForm

    def save_model(self, request, obj, form, change):
        # Ensure any custom logic or save operations handle field types correctly
        obj.save()
