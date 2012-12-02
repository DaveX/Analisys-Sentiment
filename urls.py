from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from apps.home.views import index_view

urlpatterns = patterns('',
    # Example:
    # (r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')), 
   url(r'^',include('apps.home.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)