from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#import the libraries to parse xml and strip it
import urllib2
import datetime
import xml.etree.ElementTree as ET
import feedparser

""" Brandon, since this seemed complete, I threw it in the main "transportation" view. I also made some slight changes to allow easier styling.
def septa(request):
	response = urllib2.urlopen('http://app.septa.org/nta/result.php?loc_a=Haverford&loc_z=30th+Street+Station')
	raw_html = response.read()
	final_schedule = '<h1>Haverford to 30th Street Station</h1>'
	start = raw_html.index('<div id="nta_page">')
	end = raw_html.index('</TABLE>')
	for x in range(start,end):
		final_schedule += raw_html[x]
	return HttpResponse(final_schedule)
"""


def events_upenn(request):
	raw_response = urllib2.urlopen("http://www.upenn.edu/calendar-export/?type=rss2&showndays=7").read()
        xml_response = ET.fromstring(raw_response)
        product = ''
        for child  in xml_response:
                for grandchild in child.findall('item'):
			print grandchild[0].text
                        #product += '<div style="border:solid">'
                        #product += '<h1>'+ grandchild[0].text.encode('utf-8')+'</h1>'
                        #product += '<p>'+ grandchild[1].text.encode('utf-8')+'</p>'
                        #product += '</div>'
        return HttpResponse(product)
