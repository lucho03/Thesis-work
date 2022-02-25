from django.http import JsonResponse
from main.models import AnswerModel, TicketModel
from .serializer import TicketSerializer, AnswerSerializer

tickets = TicketModel.objects.all()
serializer_tickets = TicketSerializer(tickets, many=True)
answers = AnswerModel.objects.all()
serializer_answers = AnswerSerializer(answers, many=True)

def tickets(request):
    return JsonResponse({'data':serializer_tickets.data}, status=200)

def answers(request):
    return JsonResponse({'data':serializer_answers.data}, status=200)

def data(request):
    return JsonResponse({'tickets':serializer_tickets.data, 'answers':serializer_answers.data}, status=200)