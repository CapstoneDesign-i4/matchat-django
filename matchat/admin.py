from django.contrib import admin
from .models import Product, Photo

class PhotoInline(admin.TabularInline):
    model = Photo

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = (PhotoInline,)

admin.site.register(Product, ProductAdmin)
