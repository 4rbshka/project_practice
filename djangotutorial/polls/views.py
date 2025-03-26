from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from polls.models import Question, Choice
from polls.serializers import QuestionSerializer, ChoiceSerializer

# Список вопросов
class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

# Голосование за вариант
class VoteView(APIView):
    def post(self, request, choice_id):
        try:
            choice = Choice.objects.get(id=choice_id)
            choice.votes += 1
            choice.save()
            return Response(ChoiceSerializer(choice).data, status=status.HTTP_200_OK)
        except Choice.DoesNotExist:
            return Response({"error": "Choice not found"}, status=status.HTTP_404_NOT_FOUND)
