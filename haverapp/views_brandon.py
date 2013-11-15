from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#import the libraries to parse xml and strip it
import urllib2
import datetime
import xml.etree.ElementTree as ET
import feedparser

def septa(request):
	response = urllib2.urlopen('http://app.septa.org/nta/result.php?loc_a=Haverford&loc_z=30th+Street+Station')
	raw_html = response.read()
	final_schedule = '<h1>Haverford to 30th Street Station</h1>'
	start = raw_html.index('<div id="nta_page">')
	end = raw_html.index('</TABLE>')
	for x in range(start,end):
		final_schedule += raw_html[x]
	return HttpResponse(final_schedule)

def swarthmore_events(request):
        raw_response = urllib2.urlopen("http://calendar.swarthmore.edu/calendar/RSSSyndicator.aspx?category=&location=&type=N&binary=Y&keywords=&number=20&ics=Y").read()
        xml_response = ET.fromstring(raw_response)
	product = ''
	for child  in xml_response:
		for grandchild in child.findall('item'):
			product += '<div style="border:solid">'
			product += '<h1>'+ grandchild[0].text.encode('utf-8')+'</h1>'
			product += '<p>'+ grandchild[2].text.encode('utf-8')+'</p>'
			product += '</div>'
        return HttpResponse(product)

def events_haverford(request):
	raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
        xml_response = ET.fromstring(raw_response)
        product = ''
        for child  in xml_response:
		product += u"<div style='border:solid'><div><h1>{0}</h1></div> <div>{1}</div>".format(child[0].text, child[1].text)	
		product += str(child[2].text)
		product += '<br/>' +  str(child[3].text)+'</div>'
	product += '<a href="/events/"><div style="font-size:60pt;text-align:center">Back</div></a>'

	return HttpResponse(product)

def events_bryn_mawr(request):
	return HttpResponse("Hello World")
