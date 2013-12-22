from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from models import *

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
import feedparser
from xml.etree import ElementTree

from transportation_views import *
from events_views import *

def menu_screen(request, page="index"):
 if page=="health":
  menu="health_menu.html"
  title="HaverHealth"
 elif page=="events":
  menu="events_menu.html"
  title="Events"
 elif page=="transportation":
  menu="transportation_menu.html"
  title="Transportation" 
 else:
  menu ="menu.html"
  title="HaverApp"
 return render(request, "index.html", {"title":title, "menu":menu})


#Written by Brandon on 12/12/2013
#Last Edited by Casey 12/21/2013
#Notes: Should translate this to create database entries and give THOSE to client instead.
def get_DC_menu(request, date=datetime.datetime.today()):
        message = ""
        today = date
        date_formatted  = date.strftime("%Y-%m-%d")
        date_tomorrow = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        raw_link = "http://www.google.com/calendar/feeds/hc.dining%40gmail.com/public/full?max-results=5&fields=entry(content,gd:when(@startTime))&start-min={}&start-max={}&orderby=starttime&sortorder=descending&strict=true&prettyprint=true".format(date_formatted, date_tomorrow)
        raw_feed = feedparser.parse(raw_link)

        date_time = str(date)[11:-7]
        todays_feed = ""
        
	#set the different hours and minutes for breakfast and lunch
	lunch = 11
	dinner = 17
        
	#Start to strip the feed for the requested meal:
        for entry in raw_feed.entries[2:]:
                feed = entry["content"][0]["value"]
		if "gd_when" in entry.keys():
                	start_time = entry["gd_when"]["starttime"][11:-10]
		else:
			start_time = entry["gd_when"]["starttime"][11:-10]

                #date_time = "18:30:00"
		hour = int(date_time[:2])
		mins = int(date_time[3:5])
                if hour  < lunch and start_time == "07:30:00":
			todays_feed += "<h1>Breakfast</h1>"
                        for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "
                        todays_feed += "</br>"
                        break
                elif hour >= lunch and hour  < dinner and start_time == "11:00:00":
			todays_feed += "<h1>Lunch</h1>"
                        for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "
                        todays_feed += "</br>"
                        break
                elif hour >= dinner and hour <= 24 and start_time == "17:00:00":
			todays_feed += "<h1>Dinner</h1>"
			for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "
                        todays_feed += "</br>"
                        break
	if not todays_feed:
		message="Apparently, nothing is on the menu for today!"
	return render(request, "app_container.html", {"date":date, "message":message, "title": "DC Grub", "feed":todays_feed, "template": "DC_feed.html"})



#Sample "Events" web-stripper.
#def events(request):
# raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
# xml_response = ElementTree.fromstring(raw_response)
#
# product = ""
# for i in xml_response:
#  product += u"<div>{1} {0}</div>".format(i[0].text, "Hello")
#
# return HttpResponse(product)
