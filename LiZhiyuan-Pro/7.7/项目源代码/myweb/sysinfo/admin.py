from django.contrib import admin
from .models import Message

# Register your models here.

#admin.site.register(Message)

class MessageAdmin(admin.ModelAdmin):
    list_diaplay=('title','content','email',)
    
admin.site.register(Message,MessageAdmin)