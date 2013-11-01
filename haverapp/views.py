from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree

def menu_screen(request, page="index"):
	if page=="health":
		menu="health_menu.html"
		title="HaverHealth"
	elif page=="events":
		menu="events_menu.html"
		title="Events"	
	else:
		menu ="menu.html"
		title="HaverApp"
	return render(request, "index.html", {"title":title, "menu":menu})

def events(request):
	raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
	xml_response = ElementTree.fromstring(raw_response)

	product = ""
	for i in xml_response:
		product += u"<div>{1} {0}</div>".format(i[0].text, "Hello")

	return HttpResponse(product)
	#return render(request, "events.html")
