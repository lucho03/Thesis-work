from django.contrib import admin
from django.contrib.auth.models import User
from .models import TicketModel, AnswerModel, CommentAnswerModel, CommentTicketModel, RegisterAgent
from .forms import AgentForm

'''
admin.register(TicketModel)(admin.ModelAdmin)
admin.register(AnswerModel)(admin.ModelAdmin)
admin.register(CommentAnswerModel)(admin.ModelAdmin)
admin.register(CommentTicketModel)(admin.ModelAdmin)
'''

class AdminRegisterAgent(admin.ModelAdmin):
    list_display = ('email', )
    fields = ('email',)
    change_list_template = 'admin/change_list.html'
    #add_list_template = 'admin/base_site.html'
    

admin.site.register(RegisterAgent, AdminRegisterAgent)

admin.site.register(TicketModel, admin.ModelAdmin)
admin.site.register(AnswerModel, admin.ModelAdmin)
admin.site.register(CommentTicketModel, admin.ModelAdmin)
admin.site.register(CommentAnswerModel, admin.ModelAdmin)