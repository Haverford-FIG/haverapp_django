from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from models import *

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree

import re #Import regex expressions.

def strip_table(string):
	re.sub("\s+","\s", string) #Remove multiple spaces from the "table string."
	list_table = [[]] #The table organized into list of lists (ie, [row 1, row 2, row n].
	element_stack = []

	#Variable Setup:
	get_tag, get_data, table_found, tr_found, td_found, in_tag, t_found = False, False, False, False, False, False, False

	tag_datum, cell_datum = "",""
	for i in string:
		if i=="<":
			in_tag=True
		elif i==">":
			in_tag=False
		elif in_tag and not t_found:
			if i==" ":
				element_stack.insert(0, tag_datum)
				tag_datum = ""
			elif get_tag:
				tag_datum += i
		elif get_data and not in_tag:
			cell_datum += i
		else:
			i = i.lower()
			if i == "/":
				if get_data:
					list_table[-1].append(cell_datum)
					cell_datum = ""
					get_data = False
				elif td_found:
					td_found = False
				elif tr_found:
					tr_found = False
				elif table_found:
					break #If we finish the table early, break the loop.
			#Tag-parsing options
			elif i=="t":
				t_found = True
			elif i=="a" and t_found:#Table element.
				element_stack.append("table")
				table_found = True
				t_found = False #If no valid tag is found, ignore it.
			elif i=="r" and t_found:#Row element.
				get_data = False
				tr_found = True
				element_stack.append("tr")
				list_table.append([])
				t_found = False #If no valid tag is found, ignore it.
			elif (i=="d" or i=="h") and t_found: #Column element.
				get_data = True
				td_found = True
				element_stack.append("td")
				t_found = False #If no valid tag is found, ignore it.
			else:
				if t_found: tag_datum += "t"
				get_tag = True
 
	return list_table

def find_nth(string, substring, n):
	result_index = 0
	while n>0:
		temp_index = string.index(substring)
		string = string[temp_index+1:]
		result_index += temp_index	
		n -= 1
	return result_index

#Returns a "data" dictionary for the transportation view.
def get_SEPTA_data():
	response = urllib2.urlopen('http://app.septa.org/nta/result.php?loc_a=Haverford&loc_z=30th+Street+Station')
	raw_html = response.read()
	schedule = 'Haverford to 30th Street (R100)'
	start = find_nth(raw_html, "<TABLE", 2) #... since SEPTA has a table embedded in a table.
	end = raw_html.index('</TABLE>')+8
	
	raw_table = raw_html[start:end].translate(None, "\n,\t")
	parsed_table = strip_table(raw_table)	

	return {"schedule": schedule, "table":parsed_table}

#Written by Casey Falk (12/5/13)
#Last Modified by "      "
def sort_by_name_field(query):
 parsed_entries = {}
 for entry in query:
  if entry.name in parsed_entries:
   parsed_entries[entry.name].append(entry)
  else:
   parsed_entries[entry.name] = [entry]
 return parsed_entries

#Written by Casey Falk (12/5/13)
#Last Modified by "      "
def get_blueBus_data(json_file = None):
 #Get the appropriate day of the week.
 day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][datetime.datetime.now().weekday()]

 if day=="Saturday":
  if datetime.now().time < datetime.datetime(0,0,0,15):
   day = " (Night)"
  else:
   day = " (Day)"

 #Get the data for today.
 query = BlueBusDay.objects.filter(day=day)
 parsed_entries = sort_by_name_field(query)
 schedule_table = [[heading, parsed_entries[heading]] for heading in parsed_entries.keys()]

 #Get the unique headings from the first 10 queries to use for the data. (TODO: Generalize!) 
 
 return {"day": day, "schedule_today": schedule_table}

#The main TRANSPORTATION view that funnels view information into one easy-to-use template. 
def transportation(request, page):
	if page=="SEPTA":
		template = "SEPTA.html"
		data = get_SEPTA_data()
		title="SEPTA"
	elif page=="bluebus":
		template = "blueBus.html"
		data = get_blueBus_data()
		title="Blue Bus"
	else:
		template = "blueBus.html"
		data = {"heading_1":[], "heading_2":[]}
		title="404"
	return render(request, "transportation.html", {"template":template, "data":data, "title": title})


