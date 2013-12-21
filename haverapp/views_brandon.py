from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render
from datetime import time


#import the libraries to parse xml and strip it
import urllib2
import time
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

def new_grub2(request, date=datetime.datetime.today()):
	today = date
	date_formatted  = date.strftime("%Y-%m-%d")
	date_tomorrow = today.strftime("%Y-%m-%d")
	raw_link = "http://www.google.com/calendar/feeds/hc.dining%40gmail.com/public/full?max-results=5&fields=entry(content,gd:when(@startTime))&start-min={}&start-max={}&orderby=starttime&sortorder=descending&strict=true&prettyprint=true".format(date_formatted, date_tomorrow)
        raw_feed = feedparser.parse(raw_link)
	
	date_time = str(date)[11:-7]
	print date_time
	#return HttpResponse(len(raw_feed.entries))
        feed = ""
        todays_feed = ""
	#return HttpResponse("<a href='"+raw_link+"'> Click here </a>")
	breakfast = "07:30:00"
	lunch = "11:00:00"
	dinner = "17:00:00"
        #Start to strip the feed for the requested meal:
        for entry in raw_feed.entries[2:]:
                feed = entry["content"][0]["value"]
		start_time = entry["gd_when"]["starttime"][11:-10]
		if start_time ==  breakfast  and date_time  >=  breakfast and date_time < lunch:
			print "got here"
			for x in feed:
				if not number(x):
                			todays_feed += x
				else:
					todays_feed += " "
			todays_feed += "</br>"
			break
		elif start_time == lunch and date_time < dinner and date_time >= lunch:
                        print "in lunch"
			for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "
		  	todays_feed += "</br>"
			break
		elif date_time >= dinner and start_time == dinner:
                        print "in dinner"
			print date_time
			print start_time
			for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "	
		 	todays_feed += "</br>"
			break
        return HttpResponse(todays_feed)

def number(x):
	numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
	if x in numbers:
		return True
	else:
		return False
