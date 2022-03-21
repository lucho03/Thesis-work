from django.contrib import admin
from django.contrib.auth.models import User
from .models import TicketModel, AnswerModel, CommentAnswerModel, CommentTicketModel

admin.site.register(TicketModel, admin.ModelAdmin)
admin.site.register(AnswerModel, admin.ModelAdmin)
admin.site.register(CommentTicketModel, admin.ModelAdmin)
admin.site.register(CommentAnswerModel, admin.ModelAdmin)