from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from messageboard.models import *
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from messageboard.forms import RegistrationForm

# Create your views here.
item_per_page=10

def msg_list_page(request):
    return ListView.as_view(request,queryset=MsgPost.object.order_by('-id'),
    paginate_by=item_per_page,
    page=1,
    template_name='main.html',
    template_object_name='main.html')
    
def main(request):
    posts=MsgPost.objects.all() #get all records
    return render_to_response('main.html',{'posts':posts})
    
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user( username=form.cleaned_data['username'],
                                             email=form.cleaned_data['email'],
                                             password=form.cleaned_data['password1'])
            return HttpResponseRedirect('/main/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request,{'form':form})
    return render_to_response('registration/register.html',variables)

@login_required
def msg_post_page(request):
    if request.method=='POST':
        form = MsgPostForm(request.POST)
        if form.is_valid():
            newmessage = MsgPost(title=form.cleaned_data['title'],
                             content=form.cleaned_data['content'],
                             #user=request.user
                             )
            newmessage.save()
        return HttpResponseRedirect('/main/')
    else:
        form=MsgPostForm()
    variables=RequestContext(request,{'form':form})
    return render_to_response('msg_post_page.html',variables)