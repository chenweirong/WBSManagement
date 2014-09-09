#-*- encoding:UTF-8 -*-

from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
from admin import WBSManagementAdmin
#from filebrowser.sites import site

#admin.autodiscover(site=WBSManagementAdmin)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WBSManagement.views.home', name='home'),
    # url(r'^WBSManagement/', include('WBSManagement.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
#     url(r'grappelli/',include('grappelli.urls')),

    url(r'^admin/$',lambda x:HttpResponseRedirect('/')),
    url(r'^admin/',include(WBSManagementAdmin.urls)),
#     url(r'^admin/filebrowser/',include(site.urls)),
    
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #  ??
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': '/'}),
)

if settings.DEBUG:
   urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('WBSManagement.views',
    url(r'^$','loginhtml'),
    url(r'^login$','userlogin'),
    url(r'^logout$','userlogout'),
    url(r'^validate$','validate',name='validate'),
    url(r'^workplace$','workplace'),
    url(r'^chkenv','chkenv'),
)
urlpatterns += patterns('WBSManagement.getsvrsvc',
    url(r'^getmenu$','getmenu'),
    url(r'^gettestmenu$','getStudentInfo'),
    url(r'^updpasswd$','updpassword'),
    url(r'^req$','reqentrance'),
)
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    )
