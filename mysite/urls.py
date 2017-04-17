from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from myapp1.views import wx
from myapp1.views import QAdisplay
#import myapp1.views as my_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wx$', wx.as_view(),name='my-view'),
    url(r'index$',"myapp1.views.index"),
    url(r'QAdisplay',"myapp1.views.QAdisplay"),
)
