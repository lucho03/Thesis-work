from attr import field
from rest_framework.serializers import ModelSerializer
from main.models import TicketModel, AnswerModel, CommentAnswerModel, CommentTicketModel

class TicketSerializer(ModelSerializer):
    class Meta:
        model = TicketModel
        fields = ['id', 'author', 'title', 'text', 'date', 'ticket_comments', 'priority', 'status', 'type']

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ['id', 'ticket', 'text', 'answer_comments', 'number']

class CommentAnswerSerializer(ModelSerializer):
    class Meta:
        model = CommentAnswerModel
        fields = ['answer', 'text', 'number']

class CommentTicketSerializer(ModelSerializer):
    class Meta:
        model = CommentTicketModel
        fields = ['ticket', 'text', 'number']