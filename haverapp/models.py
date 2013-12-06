from django.core import validators
from django.core.cache import cache

from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

from datetime import datetime

class BlueBusDay(models.Model):
	day = models.CharField(max_length=9)
	time = models.TimeField()
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return "{}: {} ({})".format(self.day, self.time, self.name)

#Written by Casey Falk (12/5/13)
#Last Modified by "    "
#  Store a new entry in the database with the given fields. 
def store_new_BlueBusDay_entry(day, time, name):
 new_entry = BlueBusDay()
 new_entry.day = day
 new_entry.time = time
 new_entry.name = name
 new_entry.save()

#Written by Casey Falk (12/5/13)
#Last Modified by "     "
def update_BlueBusDay_entries_on(day, data_matrix):
 try:
  #Variable Setup
  i = 1
  headers = data_matrix.pop(0) #Get the headers from the data_matrix.
  
  #Check the data_matrix type:
  if type(data_matrix)!=list:
   raise Exception("Please use the output of the organize_bus_times function as input.")
  #Completely replace the objects on the given day. 
  BlueBusDay.objects.filter(day=day).delete()    

  #Create the new database entries.
  for row in data_matrix:
   header_index = 0
   for raw_time in row:
    if not raw_time: 
     continue #Skip any entry that does not have a time.
    else:
     #If the raw_time does not have a zero-pad, add one.
     if raw_time[2]!=":": 
      raw_time = "0" + raw_time
    time = datetime.strptime(raw_time, "%I:%M%p")
    name = headers[header_index]
    store_new_BlueBusDay_entry(day, time, name)

    header_index += 1 #NOW save the BlueBusDay object to the database.
    i += 1 #Increment the total number of entries made.
  print "Database entries for \"{}\" updated successfully!".format(day)
 except Exception as e:
  raise Exception("Could not create data entry {} (\"{}\"): {}".format(i, raw_time, e))
    
#WRITTEN BY JESSE PAZDERA, LAST UPDATE: 12/5/13

def organize_bus_times(number_of_columns, times):
        current_string = ''
        current_row = []
        if number_of_columns == 4:
                timetable = [['Leave Bryn Mawr', 'Arrive Haverford', 'Leave Haverford', 'Arrive Bryn Mawr']]
        elif number_of_columns == 2:
                timetable = [['Bryn Mawr to Haverford', 'Haverford to Bryn Mawr']]
        elif number_of_columns == 5:
                timetable = [['Leaves BMC', 'Leaves Suburban Square', 'Leaves HCA', 'Leaves Stokes', 'Leaves Suburban Square']]
        else:
                raise Exception('Invalid value for parameter number_of_columns. Valid inputs are 2, 4, and 5.')
        i = ''
        for i in times:
                if len(current_row) < number_of_columns:
                        if i == '\t': #if empty box in column
                                current_row = current_row + ['']
                        else:
                                if i != 'M':
                                        if i != ' ' and i != '\n': #ignore spaces between number and AM/PM
                                                current_string = current_string + i
                                else:
                                        current_string = current_string + i
                                        current_row = current_row + [current_string]
                                        current_string = ''
                else:
                        timetable = timetable + [current_row]
                        current_row = []
        return timetable

