from django.contrib import admin

from .models import Customer, Vendor

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_type', 'acl',)

    def name(self, obj):
        return obj.user.name

    def acl(self, obj):
        return obj.user.acl.name


admin.site.register(Customer, CustomerAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'acl')

    def acl(self, obj):
        return obj.user.acl

admin.site.register(Vendor, VendorAdmin)