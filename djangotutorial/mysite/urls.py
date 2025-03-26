from django.contrib import admin
from django.urls import include, path
from rest_framework.views import APIView
from rest_framework.response import Response
from cpus.models import HardwareComponent
from cpus.serializers import HardwareComponentSerializer
from polls.views import QuestionListView, VoteView
from cpus.views import HardwareComponentsListView

class APIRootView(APIView):
    def get(self, request, format=None):
        # Получаем все аппаратные компоненты
        queryset = HardwareComponent.objects.all()
        serializer = HardwareComponentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),
    path('api/questions/', QuestionListView.as_view(), name='question-list'),
    path('api/questions/vote/<int:choice_id>/', VoteView.as_view(), name='vote'),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path('api/hardware/', HardwareComponentsListView.as_view(), name='hardware-list'),
]