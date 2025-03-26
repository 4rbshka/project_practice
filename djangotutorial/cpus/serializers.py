# cpus/serializers.py
from rest_framework import serializers
from .models import HardwareComponent

class HardwareComponentSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    release_date = serializers.DateField(format="%Y-%m-%d")
    
    class Meta:
        model = HardwareComponent
        fields = [
            'id',
            'name',
            'category',
            'category_display',
            'manufacturer',
            'release_date',
            'price',
            'power_consumption',
            'description',
            'in_stock'
        ]