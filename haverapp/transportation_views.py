from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

from models import *

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree

import re #Import regex expressions.

#Written by Casey Falk (12/20/13)
#Last Modified by "              "
#NOTES: There was a syntax error in the response, so popping element_stack has to check top.
def parse_table(table_string):
 #Wash any extra spaces from the table_string
 table_string = re.sub("\s+"," ", table_string) #Remove extra spaces from the "table string."
 table_string = re.sub(">\s",">", table_string) #Remove unnecessary spaces between tags.
 table_string = re.sub("\s<","<", table_string) #Remove unnecessary spaces between tags.
 result = []

 #Variables for Handling Tag Reading
 skip_to_end_bracket = False
 closing = False
 mid_tag = False
 matched = 0

 #Variables for Table Element Hierarchy
 element_stack = ["start"]

 for i in table_string:
  char = i.lower()
  #Ignore comments
  if element_stack[-1]=="comment":
   if matched<2 and char=="-":
    matched += 1
   elif matched==2 and char==">" and element_stack[-1]=="comment":
    element_stack.pop()
   else:
    matched = 0
  #Match tags if they are correct.
  elif mid_tag:
   #General Tag Structure
   if char==">":
    matched = 0
    mid_tag = False
    closing = False
    skip_to_end_bracket = False
   elif char==" ": #Ignore any attributes of a tag.
    skip_to_end_bracket = True

   elif skip_to_end_bracket:
    continue

   #Comment Syntax
   elif char=="!" and matched==0:
    matched += 1
   elif char=="-" and matched==1:
    matched += 1
   elif char=="-" and matched==2:
    matched=0
    element_stack.append("comment")

   #Table Element Syntax
   elif char=="t" and matched==0:
    matched += 1
   elif (char=="d" or char=="h") and matched==1: #"TD" Syntax
    matched = 0
    skip_to_end_bracket = True
    if closing:
     if element_stack[-1]=="td":
      element_stack.pop()
    else:
     result[-1].append("")
     element_stack.append("td")
   elif char=="r" and matched==1: #"TR" Syntax
    matched = 0
    skip_to_end_bracket = True
    if closing:
     if element_stack[-1]=="tr":
      element_stack.pop()
    else:
     result.append([])
     element_stack.append("tr")
   elif char=="a" and matched==1: #"TABLE" Syntax
    matched += 1
   elif char=="b" and matched==2:
    matched += 1
   elif char=="l" and matched==3:
    matched += 1
   elif char=="e" and matched==4:
    matched = 0
    skip_to_end_bracket = True
    if closing:
     if element_stack[-1]=="table":
      element_stack.pop()
    else:
     element_stack.append("table")

   elif char=="/" and matched==0:
    closing = True

  else:
   if char=="<":
    mid_tag = True
    closing = False
    matched=0
   else:
    #Append the char to the string in the current row-column entry.
    result[-1][-1] += i #The case-sensitive string.
 print result
 print "_____"
 print result[-1]
 return result

def find_nth(string, substring, n):
	result_index = 0
	while n>0:
		temp_index = string.index(substring)
		string = string[temp_index+1:]
		result_index += temp_index	
		n -= 1
	return result_index

#Returns a "data" dictionary for the transportation view.
def get_SEPTA_data(start_location="Haverford"):
 #Variable Setup
 message = ""
 schedule = "{} to 30th".format(start_location)
 response = urllib2.urlopen('http://app.septa.org/nta/result.php?loc_a={}&loc_z=30th+Street+Station'.format(start_location))
 raw_html = response.read()

 #Strip the times-table from the SEPTA response.
 start = find_nth(raw_html, "<TABLE", 2) #... since SEPTA has a table embedded in a table.
 end = raw_html.index('</TABLE>')+8 
 raw_table = raw_html[start:end].translate(None, "\n,\t")
 parsed_table = parse_table(raw_table)	

 #If there was a message rather than times, display the message.
 if len(parsed_table[1])==1:
  message = parsed_table[1][0] 
 else:
  #Do some manual choosing regarding which columns we want... 
  parsed_table = [[c,d,f] for [a,b,c,d,e,f] in parsed_table]  

 return {"schedule": schedule, "table":parsed_table, "message":message}

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

#Written by Casey Falk (12/21/13)
#Last Modified by "      "
def get_blueBus_data(date=None):
 #Variable Setup
 error = ""
 #Get the input date if possible, else show the current day.
 try:
  date = datetime.datetime.strptime(date,'%m/%d/%Y')
 except:
  date = datetime.datetime.now()
 

 #Get the appropriate day of the week.
 day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][date.weekday()]

 if day=="Saturday":
  if datetime.datetime.now().time < datetime.datetime(1,1,1,15).time:
   day += " (Night)"

 #Get the data for today.
 query = BlueBus.objects.filter(day=day)
 headings = BlueBus.objects.filter(day=day).values_list("name").distinct()
 parsed_entries = sort_by_name_field(query)
 schedule_table = [[heading, parsed_entries[heading]] for heading in parsed_entries.keys()]

 if not schedule_table:
  error = "No times left!"
 
 return {"day": day, "error":error,  "schedule_table": schedule_table, "headings":headings}

"""
def get_next_blueBuses(query, date):
 #Variable Setup
 error = ""
 #Get the input date if possible, else show the current day.
 try:
  date = datetime.datetime.strptime(date,'%m/%d/%Y')
 except:
  date = datetime.datetime.now()

 #Get the appropriate day of the week.
 day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][date.weekday()]

 if day=="Saturday":
  if datetime.datetime.now().time < datetime.datetime(1,1,1,15).time:
   day += " (Night)"

 day_options = BlueBus.objects.filter(day=day).values_list("name").distinct()

 assert()
 query = BlueBus.objects.filter(day=day)
 datetimes = sorted([datetime.datetime.strptime(entry.time, "%H:%M%p") for entry in query])
 
 result = []
"""

#The main TRANSPORTATION view that funnels view information into one easy-to-use template. 
def transportation(request, page, option=None, year="", month="", day=""):
	back="transportation"
	if page=="SEPTA":
		template = "SEPTA.html"
		data = get_SEPTA_data(option)
		if option and option=="Ardmore":
			data["other_option"]="Haverford"
		else:
			data["other_option"]="Ardmore"
		title="SEPTA"
	elif page=="bluebus":
		template = "blueBus.html"
		date = "{}/{}/{}".format(month,day,year);
		data = get_blueBus_data(date=date)
		title="Blue Bus"
	else:
		template = "blueBus.html"
		data = {"heading_1":[], "heading_2":[]}
		title="404"
	return render(request, "app_container.html", {"template":template, "data":data, "title": title, "back":back})


