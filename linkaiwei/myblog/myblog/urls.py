"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from blog.views import get_blogs, get_detail,register,mylogin,changepassword,mylogout,get_jokes

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^register/$',register,name = 'register'),
    url(r'^login/$', mylogin),
    url(r'^login/register/$', register),
    url(r'^logout/$',mylogout),
    url(r'^$', get_blogs, name='blog_get_blogs'),
    url(r'^user/(\w+)$',get_blogs),
    url(r'^changepassword/(\w+)$',changepassword,name='changepw'),
    url(r'^detail/(\d+)/$', get_detail, name='blog_get_detail'),
    url(r'^get_jokes/$', get_jokes, name='get_jokes'),
]
