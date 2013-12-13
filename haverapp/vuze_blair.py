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

def new_grub3(request, date=datetime.datetime.today()):
        today = date
        date_formatted  = date.strftime("%Y-%m-%d")
        date_tomorrow = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        raw_link = "http://www.google.com/calendar/feeds/hc.dining%40gmail.com/public/full?max-results=5&fields=entry(content,gd:when(@startTime))&start-min={}&start-max={}&orderby=starttime&sortorder=descending&strict=true&prettyprint=true".format(date_formatted, date_tomorrow)
        raw_feed = feedparser.parse(raw_link)

        date_time = str(date)[11:-7]
        todays_feed = ""
        
	#set the different hours and minutes for breakfast and lunch
	lunch = 11
	dinner = 17
        
	#Start to strip the feed for the requested meal:
        for entry in raw_feed.entries[2:]:
                feed = entry["content"][0]["value"]
                start_time = entry["gd_when"]["starttime"][11:-10]
                #date_time = "18:30:00"
		hour = int(date_time[:2])
		mins = int(date_time[3:5])
                if hour  < lunch and start_time == "07:30:00":
			todays_feed += "<h1>Breakfast</h1>"
                        for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "
                        todays_feed += "</br>"
                        break
                elif hour >= lunch and hour  < dinner and start_time == "11:00:00":
			todays_feed += "<h1>Lunch</h1>"
                        for x in feed:
                                if not number(x):
                                        todays_feed += x
                                else:
                                        todays_feed += " "
                        todays_feed += "</br>"
                        break
                elif hour >= dinner and hour <= 24 and start_time == "17:00:00":
			todays_feed += "<h1>Dinner</h1>"
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
                                         	
