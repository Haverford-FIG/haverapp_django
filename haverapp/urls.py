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
	(r"^bluebus/?$", transportation, {"page": "bluebus"}),

	(r"^dining/?$", new_grub3),	
	#Test Views that ultimately should be deleted.
	(r"^casey/?$", casey),
	(r"^anh/?$", anh),
	(r"^fortytwo/?$", fortytwo),
	(r"^brandon/?$", new_grub3),
	#(r"^jesse/?$", jesse),
	(r"^caleb/?$", caleb),
	(r"^dawit/?$", dawit),
	(r"^blair/?$", new_grub2),
	(r"^camp_philly_feed/?$", camp_philly_feed),


	
    # Uncomment the next line to enable the admin:
    	(r'^admin/', include(admin.site.urls)),
)
