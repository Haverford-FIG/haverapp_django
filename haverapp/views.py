from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from models import *

#Import the libraries to parse xml and strip it.
import numpy
import urllib2
import datetime
import feedparser
from xml.etree import ElementTree

from transportation_views import *
from events_views import *
from news_views import *


def main_page(request):
 	return render(request, "index.html")




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
 elif page=="studentnews":
  menu="student_news.html"
  title="Student News" 
 else:
  menu ="menu.html"
  title="HaverApp"
 return render(request, "index.html", {"title":title, "menu":menu})


#Written by Brandon on 12/12/2013
#Last Edited by Casey 12/21/2013
#Notes: Should translate this to create database entries and give THOSE to client instead.

def remove_dups(l):
	s = []
	for x in l:
		if x not in s:
			s.append(x)
		
	return list(set(l))

def get_DC_menu(request, date=datetime.datetime.today() + datetime.timedelta(days=0)):
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
    	final = []
	for entry in raw_feed.entries:
                feed = entry["content"][0]["value"]
		time = entry["gd_when"]["starttime"][11:13]
		counter = 0
		for x in feed:
                	if not number(x):
        	                todays_feed += x
                        else:
				if counter%4 == 0:
                                	todays_feed += "<br>"
				counter = counter + 1
		
		final.append([todays_feed, time])
		todays_feed = ""

	todays_feed = ""
	
	while len(final) > 3:
		final = final[1:]
	

	if len(final) > 1:
		for x in final:
			if x[1] == "07":
				todays_feed += "<h2>Breakfast</h2>" + x[0][4:]
		for x in final:
			if x[1] == "11":
				todays_feed += "<h2>Lunch</h2>" + x[0][4:]
			elif x[1] == "10":
				todays_feed +=  "<h2>Brunch</h2>" + x[0]
		for x in final:
			if x[1] == "17":
				todays_feed += "<h2>Dinner</h2>" + x[0][4:]
	elif len(final) == 2:
		todays_feed += "<h2>Brunch</h2>" + final[1][0][4:]
		todays_feed += "<h2>Dinner</h2>" + final[0][0][4:]
	else:
		todays_feed += "<h2>Breakfast</h2>" + final[0][4:]

	if not todays_feed:
		message="Apparently, nothing is on the menu for today!"
	return render(request, "app_container.html", {"date":date, "message":message, "title": "DC Grub", "feed":todays_feed, "template": "DC_feed.html"})


def number(x):
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        if x in numbers:
                return True
        else:
                return False

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
