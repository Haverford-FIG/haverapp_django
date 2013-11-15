from django.http import HttpResponse, Http404
from django.http import HttpResponse, Http404

from django.template import RequestContext
from django.shortcuts import render

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree


def dawit(request):
	return HttpResponse("")

#def  health(request):
        #return render(request, "health.html")


def haverford_events(request):
        raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
        xml_response = ElementTree.fromstring(raw_response)

        product = []  #dict()
        for i in xml_response:
		#i = []
                product.append({"name":i[0].text })
		for j in range(0, len(i)):
			product.append(i[j].text)
		#product += u"<div style='color:red; font:20px'>{1} {0}</div>".format(i[0].text,)
	
        return HttpResponse(product)
        return render(request, "events.html", {"product":product})

	


