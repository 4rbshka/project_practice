from rest_framework import renderers
import csv
from io import StringIO

class CSVRenderer(renderers.BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if data is None:
            return ''
        
        # Если это список
        if isinstance(data, list):
            if not data:
                return ''
            
            # Получаем заголовки из первого элемента
            headers = data[0].keys()
            
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            
            for row in data:
                writer.writerow(row)
            
            return output.getvalue()
        
        # Если это словарь (один объект)
        elif isinstance(data, dict):
            headers = data.keys()
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerow(data)
            return output.getvalue()
        
        return ''