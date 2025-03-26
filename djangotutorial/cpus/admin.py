from django.contrib import admin
from .models import HardwareComponent

@admin.register(HardwareComponent)
class HardwareComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'price', 'in_stock')
    list_filter = ('category', 'manufacturer', 'in_stock')
    search_fields = ('name', 'manufacturer', 'description')
    list_editable = ('price', 'in_stock')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'manufacturer', 'description')
        }),
        ('Технические характеристики', {
            'fields': ('release_date', 'power_consumption')
        }),
        ('Коммерческая информация', {
            'fields': ('price', 'in_stock')
        }),
    )