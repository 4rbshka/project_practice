import csv
import os
from django.core.management.base import BaseCommand
from cpus.models import Product
from datetime import datetime

class Command(BaseCommand):
    help = "Импортирует данные из CSV в модель Product"

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join("data", "dataset.csv")  # Путь к файлу

        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"Файл {csv_file_path} не найден!"))
            return

        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                # Фильтрация пустых данных
                product_name = row.get("Product", "").strip()
                if not product_name:
                    continue  # Пропускаем строки без названия

                # Обработка даты (если есть)
                release_date = None
                date_str = row.get("Release Date", "").strip()
                if date_str and date_str.lower() not in ["n/a", "", "none"]:
                    try:
                        release_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        self.stderr.write(self.style.WARNING(f"Некорректная дата: {date_str}"))

                # Функция для обработки числовых данных (целых и дробных)
                def parse_int(value):
                    try:
                        return int(value) if value.strip() and value.lower() not in ["n/a", "none", ""] else None
                    except ValueError:
                        return None

                def parse_float(value):
                    try:
                        return float(value) if value.strip() and value.lower() not in ["n/a", "none", ""] else None
                    except ValueError:
                        return None

                # Создание или обновление записи в БД
                product, created = Product.objects.update_or_create(
                    product=product_name,
                    defaults={
                        "type": row.get("Type", "").strip()[:3],
                        "release_date": release_date,
                        "foundry": row.get("Foundry", "").strip() or None,
                        "vendor": row.get("Vendor", "").strip() or None,
                        "process_size": parse_int(row.get("Process Size (nm)", "")),
                        "tdp": parse_int(row.get("TDP (W)", "")),
                        "die_size": parse_float(row.get("Die Size (mm^2)", "")),
                        "transistors": parse_int(row.get("Transistors (million)", "")),
                        "freq": parse_int(row.get("Freq (MHz)", "")),
                        "fp16_gflops": parse_float(row.get("FP16 GFLOPS", "")),
                        "fp32_gflops": parse_float(row.get("FP32 GFLOPS", "")),
                        "fp64_gflops": parse_float(row.get("FP64 GFLOPS", "")),
                    }
                )

                count += 1
                action = "Создан" if created else "Обновлён"
                self.stdout.write(self.style.SUCCESS(f"{action}: {product.product}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Импорт завершён! Обработано {count} записей."))
