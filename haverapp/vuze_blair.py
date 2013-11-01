from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#import the following libraries to parse xml and strip it.
import urllib2
import datetime
from  xml.etree import ElementTree
def blair(request):
	raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
	xml_response = ElementTree.fromstring(raw_response)
	product = ""
	for i in xml_response:
		product += u"<div style=border:solid;>{1}</div> <div>{0}</div>".format(i[0].text, i[1].text)
	return HttpResponse(product)
	#return render(request, "events.html")

