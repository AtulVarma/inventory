from django.contrib import admin
from .models import Category, Product
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name','price','available','created','updated']
    list_editable = ['price','available']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20

admin.site.register(Product, ProductAdmin)
