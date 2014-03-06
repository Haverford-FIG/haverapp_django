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
	#Check out Regular Expressions for more on the ^ and $ characters. --Casey
	(r"^$", menu_screen, {}),
	(r"^home/?$", menu_screen, {"page": "index"}),
	(r"^health/?$", menu_screen, {"page": "health"}),
	
	(r"^events?/?$", menu_screen, {"page": "events"}),
	(r"^events_haverford?/?$", events, {"page": "haverford"}),
	(r"^events_bryn_?mawr?/?$", events, {"page": "brynmawr"}),
	(r"^events_swarthmore?/?$", events, {"page": "swarthmore"}),
	(r"^events_upenn/?$", events, {"page": "upenn"}),
	(r"^events_campus_philly/?$", events, {"page": "campus_philly"}),
	(r"^transportation/?$", menu_screen, {"page": "transportation"}),
	(r"^SEPTA/?$", transportation, {"page": "SEPTA", "option":"Haverford"}),
	(r"^SEPTA_[Hh]averford/?$", transportation, {"page": "SEPTA", "option":"Haverford"}),
	(r"^SEPTA_[aA]rdmore/?$", transportation, {"page": "SEPTA", "option":"Ardmore"}),
	(r"^[bB]lue[bB]us/?$", transportation, {"page": "bluebus"}),
	(r"^[bB]lue[bB]us/(?P<month>\d{2})/(?P<day>\d{2})/(?P<year>\d{4})/?$", transportation, {"page": "bluebus"}),
#	(r"^studentnews/?$", studentnews, {"page":"studentnews"}),
	(r"^dining/?$", get_DC_menu),	
	#Test Views that ultimately should be deleted.
	(r"^camp_philly_feed/?$", camp_philly_feed),

	(r"^my_main_page/?$", main_page),
	
    # Uncomment the next line to enable the admin:
    	(r'^admin/', include(admin.site.urls)),
)
