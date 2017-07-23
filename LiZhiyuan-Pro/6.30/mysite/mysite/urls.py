"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from learn import views as learn_views
from calc import views as calc_views
from learn2 import views as learn2_views
from django.contrib import admin
from messageboard.views import main,register_page
#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.contrib.auth.views import login,logout
from django.contrib.auth.views import password_change,password_change_done
from messageboard.views import msg_post_page

admin.autodiscover()

urlpatterns = [
    url(r'^$', calc_views.index, name='home'),
    url(r'^sysinfo$', learn2_views.home, name='home'),
    url(r'^add/$', calc_views.add, name='add'),
    url(r'^add/(\d+)/(\d+)/$', calc_views.old_add2_redirect), 
    url(r'^jiafa/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
    url(r'^add/(\d+)\+(\d+)/$', calc_views.add2, name='add3'),
    url(r'^admin/', admin.site.urls),
    url(r'^main/$', main),
    url(r'^main/register/$', register_page),
    url(r'^main/register/success/$',TemplateView,{'template': 'register_success.html'}),
    url(r'^accounts/login/$', login),
    url(r'^main/logout/$',logout,{'next_page':'/main/'}),
    url(r'^main/password/change/$', password_change,{'template_name':'registration/password_change.html'}),
    url(r'main/password/change/done/$', password_change_done,{'template_name':'registration/password_change_success.html'}),  
    url(r'^main/post/$', msg_post_page),
]
