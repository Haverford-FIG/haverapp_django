from django.conf.urls import *

#Import HaverApp Functions here --Casey

from haverapp.views import *



from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	(r"^$", home_screen),
	(r"^events$", events_page),

    # Uncomment the next line to enable the admin:
    	(r'^admin/', include(admin.site.urls)),
)
