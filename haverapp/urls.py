from django.conf.urls import *

#Import HaverApp Functions here --Casey

from haverapp.views import *
from haverapp.views_casey import *
from haverapp.views_brandon import *
from haverapp.views_fortytwo import *
from haverapp.views_Dawit import *
from haverapp.views_caleb import *
from haverapp.views_anh import *
from haverapp.views_jesse import *
from haverapp.vuze_blair import *



from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r"^$", menu_screen, {}),
	(r"^home/?$", menu_screen, {"page": "index"}),
	(r"^main/?$", menu_screen, {"page": "index"}),
	#Check out Regular Expressions for more on the ^ and $ characters. --Casey
	(r"^event[s]?/?$", menu_screen, {"page": "events"}),
	(r"^health/?$", menu_screen, {"page": "health"}),

	(r"^casey$", casey),
	(r"^anh$", anh),
	(r"^fortytwo$", fortytwo),
	(r"^brandon$", brandon),
	(r"^jesse$", jesse),
	(r"^caleb$", caleb),
	(r"^dawit$", dawit),
	(r"^blair$", blair),
	
	
    # Uncomment the next line to enable the admin:
    	(r'^admin/', include(admin.site.urls)),
)
