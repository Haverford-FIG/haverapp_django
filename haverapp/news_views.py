from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from models import *

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree
from django.utils.html import strip_tags


import re #Import regex expressions.

def haverford_news():
	raw_response = urllib2.urlopen("http://www.haverford.edu/news/rss/").read()
	xml_response = ElementTree.fromstring(raw_response)
	product=[{"title":strip_tags(grandchild[0].text),"description":strip_tags(grandchild[1].text),"url":strip_tags(grandchild[3].text), "pubDate":strip_tags(grandchild[2].text[:17])} for child in xml_response for grandchild in child.findall("item")]
	return product



#The main EVENTS view that funnels view information into one easy-to-use template.
def news(request, page):
    template = "event_grid.html"
    if page=="haverfordnews":
        data = haverford_news()
        title="Haverford"
     
    else:
        return HttpResponse("News not found!")

    new_data = [[None, list()]]
    for entry in data:
	if "date" in entry.keys():
	    date = entry["date"]
	elif "category" in entry.keys():
	    date = entry["category"]
	elif "pubDate" in entry.keys():
	    date = entry["pubDate"]
	elif "description" in entry.keys():
	    date = entry["description"]
        if new_data[-1][0]==date:
            new_data[-1][1].append(entry)
        else:
	    if "date" in entry.keys():# works for haverford events
		new_data.append([entry["date"], [entry]])
	    elif "category" in entry.keys(): #this is for the swat events
		new_data.append([entry["category"], [entry]])
	    elif "pubDate" in entry.keys(): # this is for Bryn Mawr events
		new_data.append([entry["pubDate"], [entry]])
	    elif "description" in entry.keys(): #works for byrn mawr, but also a good default
		new_data.append([entry["description"], [entry]])

    new_data.pop(0)
    return render(request, "app_container.html", {"template":template, "data":new_data, "title": title}    )


