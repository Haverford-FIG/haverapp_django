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


#written by blair last edited by blair 12/05/2013
def new_grub(request, date=datetime.datetime.today()):
	raw_feed = feedparser.parse("http://www.google.com/calendar/feeds/hc.dining%40gmail.com/public/full?max-results=5&fields=entry(content,gd:when(@startTime))&start-min=2013-12-07&start-max=2013-12-08&orderby=starttime&sortorder=descending&strict=true&prettyprint=true")
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
		if grub_of_the_day == format_date_to_feed:  #asks if the day of today matches date on feed
			todays_feed = feed #if yes add things to todays feed
	return HttpResponse(todays_feed)

#written by blair. last edited by blair 12/05/2013
def camp_philly_feed(request):
	raw_response = urllib2.urlopen("http://campusphilly.org/feed/").read()
        xml_response = ElementTree.fromstring(raw_response)
	
	product = []
        for child  in xml_response:
                for grandchild in child.findall('item'):
                       for great_grand in grandchild:
				if great_grand.tag == "title":	
                        		title =  great_grand.text.encode('utf-8')
				elif great_grand.tag == "link":
					link = great_grand.text.encode('utf-8')
				elif great_grand.tag == "description":
					description = great_grand.text.encode('utf-8')
				final_product = {"title": title, "url": link, "description": description}
				product.append(final_product) 	
                        #product += '<p>'+ grandchild[1].text.encode('utf-8')+'</p>'
        #return HttpResponse(product)
	
	return product
	#return product	
