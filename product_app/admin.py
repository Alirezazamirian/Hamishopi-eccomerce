from django.contrib import admin
from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['car', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_editable = ['price', 'is_active']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
admin.site.register(models.Brand)
admin.site.register(models.Car)
admin.site.register(models.ProductComment)
