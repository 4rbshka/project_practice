from django.db import models
from django.core.validators import MinValueValidator

class HardwareComponent(models.Model):
    CATEGORY_CHOICES = [
        ('CPU', 'Процессор'),
        ('GPU', 'Видеокарта'),
        ('RAM', 'Оперативная память'),
        ('SSD', 'Накопитель SSD'),
        ('HDD', 'Жесткий диск'),
        ('MB', 'Материнская плата'),
        ('PSU', 'Блок питания'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название компонента")
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория"
    )
    manufacturer = models.CharField(max_length=100, verbose_name="Производитель")
    release_date = models.DateField(null=True, blank=True, verbose_name="Дата выхода")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена (USD)"
    )
    power_consumption = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name="Потребляемая мощность (Вт)"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "hardware_components"
        verbose_name = "Аппаратный компонент"
        verbose_name_plural = "Аппаратные компоненты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_category_display()}: {self.name} ({self.manufacturer})"