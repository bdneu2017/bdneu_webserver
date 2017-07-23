from django.db import models
from django.contrib import admin

# Create your models here.

class MsgPost(models.Model):
    user=models.CharField(max_length=12)
    email=models.EmailField(blank=True)
    title=models.CharField(max_length=30)
    content=models.TextField()
    datetime=models.DateField(auto_now_add=True)
    class Meta:
        ordering =['-datetime']
        
class MsgPostAdmin(admin.ModelAdmin):
    list_display = ('title','datetime','user')
    
admin.site.register(MsgPost, MsgPostAdmin)

