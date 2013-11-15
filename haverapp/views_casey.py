from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree

#Get a uniform heading given any Blue Bus-related heading.
def get_relative_heading(heading):
        try:
		heading=heading.lower()
                
		if heading=="brynmawrtohaverford": return "Leave BMC"
                if heading=="haverfordtobrynmawr": return "Leave HC"
                
		if "sub" in heading: parsed_heading="Suburban to "
                elif "leav" in heading: parsed_heading="Leave "
                elif "arri" in heading: parsed_heading="Arrive "
                
                if "hav" in heading: parsed_heading+="HC"
                elif "bryn" in heading: parsed_heading+="BMC"
                elif "bmc" in heading: parsed_heading+="BMC"
                elif "hca" in heading: parsed_heading+= "HCA"
                elif "stok" in heading: parsed_heading+= "Stokes"        
                
		assert(parsed_heading)
                return parsed_heading
        except:
                raise Exception("Unknown Heading: {}".format(heading))

def casey(request, date=datetime.datetime.today(), option="LeaveHaverford", time=None):
        error = ""
        try:
                try:
                        day = "{0:%A}".format(date)
                except:
                        day = date
                #Setup initial variables:
                next_buses = []
                schedule_today = []
                select_menu = ""
                error = ""
                
                #Parse the option.
                rel_option=get_relative_heading(option.lower())

                
		#Get all the bus times.
                all_bus_times = None#cache.get("blueBusApp|times") #Try to get the cached times.
		if not all_bus_times:
                        try:
                                raw_response = urllib2.urlopen("http://www.brynmawr.edu/transportation/bico.shtml").read()
			except:
                                error="Could not connect to the interwebs..."
                                raise
                        raw_response = raw_response.translate(None, "\t\r ").replace("</a><h3","</a>\n<h3")
                        raw_response = raw_response.replace("\n\n","\n")
                        raw_response = raw_response.replace("eaves\n","eaves").replace("urban\n","urban")
			raw_response = raw_response.split("\n")
                        all_bus_times = {}
                        row_data = []
                        store_data = False
                        found_data = False
                        in_table=False
			for line in raw_response:
                                notes = ""
                                #Add an entry to the database.
                                if line=="": continue
                                elif line[:3]=="<h3":
                                        #Get the text between the tags.
                                        heading = strip_tag(line)
                                        store_data = True
                                        if heading=="Schedules": #When we have reached the "Schedules" heading.
                                                found_data = True
                                        elif found_data:
                                                heading = heading.replace("Daytime", " (Day)").replace("Night", " (Night)")
                                                all_bus_times[heading] = [] #Remember the heading if we found_data.
                                elif not found_data: #Don't parse any more data than we need to.
                                        continue  
                                elif line[:4]=="<tab":
                                        in_table=True
                                elif line[:4]=="</ta":
                                        in_table=False
                                elif in_table:
                                        if line[:3]=="<tr":
                                                store_data = True
                                                row_data = [] #Refresh the row_data.
                                        elif line[:4]=="</tr":
                                                store_data = False
                                                if row_data: 
                                                        all_bus_times[heading].append(row_data) #Record the row_data.
                                        elif line[:3]=="<h4":
                                                store_data=False
                                        elif store_data:
                                                data = strip_tag(line)
                                                if not all_bus_times[heading]: 
                                                        data = get_relative_heading(data) #Get the heading for the row.
                                                        if "Suburban" in data:
                                                                if "Suburban to HCA" in row_data:
                                                                        data = "Suburban to BMC"
                                                                else:
                                                                        data = "Suburban to HCA"
                                                if data[:4]=="<str": 
                                                        notes="(S)"
                                                        data = strip_tag(data)
                                                row_data.append("{}{}".format(data, notes))
                        cache.set("blueBusApp|times", all_bus_times, 604800) #Cache for one week.
                
		 #Convert the time into a usable format.        
                if not time:
                        time = datetime.datetime.now().time() #Get the current time. 
                else:
                        try:
                                time = datetime.datetime.strptime(time, "%I:%M%p").time()
                        except:
                                error = "Invalid time!"
                                raise
                                
                #Make sure the correct Saturday schedule is chosen:
                if "Saturday" in day:
                        if time <= datetime.datetime.strptime("5:00PM", "%I:%M%p").time():
                                day = "Saturday (Day)"
                        else:
                                day = "Saturday (Night)"
                
                #Construct the select menu.
                select_menu = "<select class=\"blueBusSelectMenu blueBusInput\">"
                if day in {"Saturday (Night)","Sunday"}:
                        options = ["Leave Haverford", "Leave Bryn Mawr"]
                elif day=="Saturday (Day)":
                        options = ["Leave BMC", "Suburban to HCA", "Leave HCA", "Leave Stokes", "Suburban to BMC"]
                else:
                        options = ["Leave Haverford", "Arrive Haverford", "Leave Bryn Mawr", "Arrive Bryn Mawr"]
                for opt in options:
                        if opt == rel_option:
                                select_menu += "<option selected>{}</option>".format(opt)
                        else:
                                select_menu += "<option>{}</option>".format(opt)
                select_menu += "</select>"
                
                ###print all_bus_times
                #Find the next few bus times. ###Midnight bus?
                try:
                        rel_col = all_bus_times[day][0].index(rel_option)
                except:
                        rel_option = options[0] #If an option isn't found, revert to a default.
                        rel_col = all_bus_times[day][0].index(rel_option)
                next_buses = []
                batch_size = 4
                for row in all_bus_times[day][1:]: #Read all but the heading row.
                        if len(next_buses)==batch_size: break
                        
                        data = row[rel_col].replace("(", " (").split(" ")
                        note = ""
                        #Check for notes.
                        if len(data)>1:
                                if data[1]=="(S)": note=" (Sweeper)"
                        data = data[0]
                                
                        #Only collect a few of the next_buses.
                        try:
                                schedule_time = datetime.datetime.strptime(data, "%I:%M%p").time()
                                if time < schedule_time: #Assumes times are in order from AM to PM.
                                        next_buses.append("{}{}".format(data, note))
                        except:
                                continue #Skip any unparsable rows.
                
                #Format the time:
                time = time.strftime("%I:%M%p")
                if time[0]=="0": time=time[1:] #Remove the preceding "0" if applicable.

                #Get the entire schedule for today.
                schedule_today = []
                for row in all_bus_times[day]:
                        new_row = []
                        for entry in row:
                                if "(S)" in entry:
                                        entry = "<div class=\"blueBusSweeper\">{}</div>".format(entry.replace("(S)",""))
                                new_row.append(entry)
                        schedule_today.append(new_row)
                        
        except Exception as e:
                print e
                if error=="":
                        error = "Oops... Something broke... Email FIG."
        
        
        return render(request, "blueBus.html", {
                "error": error,
                "next_buses": next_buses,
                "schedule_today":schedule_today,
                "date": day,
                "select_menu": select_menu,
                "time": time
	})
