from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from models import *

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
	elif page=="transportation":
		menu="transportation_menu.html"
		title="Transportation"	
	else:
		menu ="menu.html"
		title="HaverApp"
	return render(request, "index.html", {"title":title, "menu":menu})

def transportation(request, page):
	if page=="SEPTA":
		template = "SEPTA.html"
		data = {"heading_1":[], "heading_2":[]}
		title="SEPTA"
	elif page=="bluebus":
		template = "blueBus.html"
		data = {"heading_1":[], "heading_2":[]}
		title="Blue Bus"
	else:
		template = "blueBus.html"
		data = {"heading_1":[], "heading_2":[]}
		title="404"
	return render(request, "transportation.html", {"template":template, "data":data, "title": title})

#Sample "Events" web-stripper.
#def events(request):
#	raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
#	xml_response = ElementTree.fromstring(raw_response)
#
#	product = ""
#	for i in xml_response:
#		product += u"<div>{1} {0}</div>".format(i[0].text, "Hello")
#
#	return HttpResponse(product)
