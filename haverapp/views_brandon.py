from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#import the libraries to parse xml and strip it
import urllib2
import datetime
from xml.etree import ElementTree

def brandon(request):
	try:
	   raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
	   xml_response = ElementTree.fromstring(raw_response)
	except:
	   error = "Could not connect to the internet. Sucks..."
	   raise
	
	product = "<body style='background-color:green;'>"
	for i in xml_response:
		product +=  u"<div style='border:solid;color:red;background-color:blue;'>{} </div> <br/> <h1>{}</h1>".format(i[0].text,i[1].text)
	product += "</body>"
	return HttpResponse(product)



