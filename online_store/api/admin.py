from django.contrib import admin
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'number_of_products', 'revenue']

    @admin.display
    def number_of_products(self, obj):
        return obj.products.count()

    @admin.display
    def revenue(self, obj):
        return sum([product.price for product in obj.products.all()])
