import imp
from django.contrib import admin
from .models import TicketModel, AnswerModel, CommentAnswerModel, CommentTicketModel

admin.register(TicketModel)(admin.ModelAdmin)
admin.register(AnswerModel)(admin.ModelAdmin)
admin.register(CommentAnswerModel)(admin.ModelAdmin)
admin.register(CommentTicketModel)(admin.ModelAdmin)