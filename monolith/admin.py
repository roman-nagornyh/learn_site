from django.contrib import admin
from .models import *


class TypeProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_display_links = ('id',)
    search_fields = ('name', 'price')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'sale')
    list_display_links = ('id',)

    def get_username(self, obj):
        return obj.user.username


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product_name', 'price', 'get_username',)
    list_display_links = ('id',)
    search_fields = ('get_product_name', 'get_username',)

    def get_product_name(self, obj):
        return obj.product.name

    def get_username(self, obj):
        return obj.user.username


admin.site.register(TypeProduct, TypeProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
# admin.site.register(Order, OrderAdmin)
