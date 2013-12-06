from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#import the following libraries to parse xml and strip it.
import urllib2
import datetime
from  xml.etree import ElementTree
import feedparser


def blair(request):
	raw_response = urllib2.urlopen("http://www.haverford.edu/goevents/").read()
	xml_response = ElementTree.fromstring(raw_response)
	product = ""
	for i in xml_response:
		product +=  u"<div style=border:solid;>{1}</div> <div>{0}</div>".format(i[0].text, i[1].text)

	return HttpResponse(product)
	#return render(request, "events.html")


#
def new_grub(request, date=datetime.datetime.today()+datetime.timedelta(days=1)):
	raw_feed = feedparser.parse("http://www.google.com/calendar/feeds/hc.dining@gmail.com/public/basic/")
	format_date_to_feed = "{0:%a}{0:%b}{0:%d},{0:%Y}".format(date) #puts the date into a feed-like format
	date = date.strftime("%d-%m-%Y") #This is the date that will show on the template	


	feed = ""
	todays_feed = ""
        #Start to strip the feed for the requested meal:
        for entry in raw_feed.entries:
		feed = entry["content"][0]["value"].replace("When: ", "")
		grub_of_the_day = "".join(feed[:16].split(" ")) #Remove punctuation from date for comparison.
		#todays_feed += grub_of_the_day
		#print format_date_to_feed
		print grub_of_the_day
		if grub_of_the_day == format_date_to_feed:
			todays_feed = feed
	return HttpResponse(todays_feed)

	
