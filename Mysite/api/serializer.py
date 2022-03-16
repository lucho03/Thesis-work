from rest_framework.serializers import ModelSerializer
from main.models import TicketModel, AnswerModel, CommentAnswerModel, CommentTicketModel

class TicketSerializer(ModelSerializer):
    class Meta:
        model = TicketModel
        fields =[   
                    'id', 
                    'author_username', 
                    'title', 
                    'text', 
                    'clear_text', 
                    'date', 
                    'ticket_comments', 
                    'priority', 
                    'status', 
                    'type', 
                    'num_answers', 
                    'file', 
                    'is_from_email'
                ]

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = AnswerModel
        fields =[
                    'id', 
                    'author_username', 
                    'ticket', 
                    'title', 
                    'text', 
                    'clear_text',
                    'answer_comments', 
                    'number', 
                    'lock'
                ]

class CommentAnswerSerializer(ModelSerializer):
    class Meta:
        model = CommentAnswerModel
        fields =[
                    'answer', 
                    'text', 
                    'number'
                ]

class CommentTicketSerializer(ModelSerializer):
    class Meta:
        model = CommentTicketModel
        fields =[
                    'ticket', 
                    'text', 
                    'number'
                ]