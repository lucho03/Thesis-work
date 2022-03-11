from django.contrib import admin
from django.contrib.auth.models import User
from .models import TicketModel, AnswerModel, CommentAnswerModel, CommentTicketModel, RegisterAgent
from .forms import AgentForm

admin.register(TicketModel)(admin.ModelAdmin)
admin.register(AnswerModel)(admin.ModelAdmin)
admin.register(CommentAnswerModel)(admin.ModelAdmin)
admin.register(CommentTicketModel)(admin.ModelAdmin)

class AdminRegisterAgent(admin.ModelAdmin):
    fields = ('email',)
    #def get_form(self, request, obj=None, **kwargs):
    #    print(request.user)
    

admin.site.register(RegisterAgent, AdminRegisterAgent)