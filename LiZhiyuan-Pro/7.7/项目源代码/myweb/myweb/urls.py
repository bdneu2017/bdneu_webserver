"""myweb URL Configuration

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
from sysinfo import views as sysinfo_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',sysinfo_views.index,name='index'),
    url(r'^info/',sysinfo_views.get_info,name='get_info'),
    url(r'^messageboard/',sysinfo_views.messageboard,name='messageboard'),
    url(r'^form/',sysinfo_views.test,name='add_form'),
    url(r'^add/$', sysinfo_views.add, name='add'),
    url(r'^django_forms/',sysinfo_views.djForm,name='djforms'),
    url(r'^django_ajaxs1/',sysinfo_views.djAjax_index,name='djajax1'),
    url(r'^django_ajaxs2/',sysinfo_views.djAjax_index2,name='djajax2'),
    url(r'^ajax_list/$', sysinfo_views.ajax_list, name='ajax-list'),
    url(r'^ajax_dict/$', sysinfo_views.ajax_dict, name='ajax-dict'),
    url(r'^email/$', sysinfo_views.email, name='email'),
    url(r'base_models/',sysinfo_views.base,name='base'),
    url(r'form2db/',sysinfo_views.forms2db),
    url(r'^accounts/login/',sysinfo_views.accounts,name="accounts"),
    url(r'^login/',sysinfo_views.check_user,name='login'),
    #url(r'^login/',sysinfo_views.login,name='login'),
    url(r'^registration/',sysinfo_views.register,name='registration'),
     url(r'^regist/',sysinfo_views.regist,name='regist'),
    ]