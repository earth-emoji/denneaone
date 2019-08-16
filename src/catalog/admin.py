from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Category, Product, Reservation

# Register your models here.
admin.site.register(Category)
admin.site.register(Reservation)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'vendor', 'acl', 'is_aux')

    def vendor(self, obj):
        return obj.vendor.business_name

    def acl(self, obj):
        return obj.acl.name

admin.site.register(Product, ProductAdmin)