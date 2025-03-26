from .renderers import CSVRenderer  # Импортируем наш рендерер
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView
from .models import HardwareComponent
from .serializers import HardwareComponentSerializer

class HardwareComponentsListView(ListAPIView):
    queryset = HardwareComponent.objects.all()
    serializer_class = HardwareComponentSerializer
    renderer_classes = [JSONRenderer, CSVRenderer]  # Используем наш рендерер