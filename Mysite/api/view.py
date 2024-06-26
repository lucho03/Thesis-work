from django.http import JsonResponse, HttpResponse
from main.models import AnswerModel, CommentAnswerModel, CommentTicketModel, TicketModel
from .serializer import TicketSerializer, AnswerSerializer, CommentAnswerSerializer, CommentTicketSerializer
from main.emails import send_invitation_email
from django.views.decorators.csrf import csrf_exempt

tickets = TicketModel.objects.all()
serializer_tickets = TicketSerializer(tickets, many=True)

answers = AnswerModel.objects.all()
serializer_answers = AnswerSerializer(answers, many=True)

comments_answer = CommentAnswerModel.objects.all()
serializer_comments_1 = CommentAnswerSerializer(comments_answer, many=True)

comments_ticket = CommentTicketModel.objects.all()
serializer_comments_2 = CommentTicketSerializer(comments_ticket, many=True)


def tickets(request):
    return JsonResponse({'data':serializer_tickets.data}, status=200)

def answers(request):
    return JsonResponse({'data':serializer_answers.data}, status=200)

def comments_answer(request):
    return JsonResponse({'data':serializer_comments_1.data}, status=200)

def comments_ticket(request):
    return JsonResponse({'data':serializer_comments_2.data}, status=200)

def data(request):
    return JsonResponse(
                            {
                            'tickets':serializer_tickets.data, 
                            'answers':serializer_answers.data,
                            'comments_answer':serializer_comments_1.data,
                            'comments_ticket':serializer_comments_2.data
                            }, 
                            status=200
                        )

@csrf_exempt
def invitation(request):
    try:
        email = request.body.decode()
        # send_invitation_email(email)
    except Exception:
        pass
        return HttpResponse('Invalid email!')
    return HttpResponse('OK!')