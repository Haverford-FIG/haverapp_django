from django.core import validators
from django.core.cache import cache

from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

from datetime import datetime

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Helper Functions   # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#FUNCTION WRITTEN BY JESSE PAZDERA, LAST UPDATE: 12/7/13
def org_times(number_of_columns, times):
	current_string = ''
	current_row = []
	timetable = []
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Blue Bus # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class BlueBus(models.Model):
	day = models.CharField(max_length=9)
	time = models.TimeField()
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return "{}: {} ({})".format(self.day, self.time, self.name)

#Written by Casey Falk (12/5/13)
#Last Modified by "    "
#  Store a new entry in the database with the given fields. 
def store_BlueBus_entry(day, time, name):
 new_entry = BlueBus()
 new_entry.day = day
 new_entry.time = time
 new_entry.name = name
 new_entry.save()

#Written by Casey Falk (12/5/13)
#Last Modified by "     "
def update_BlueBus_db(day, data_matrix):
 try:
  #Variable Setup
  i = 1
  headers = data_matrix.pop(0) #Get the headers from the data_matrix.
  
  #Check the data_matrix type:
  if type(data_matrix)!=list:
   raise Exception("Please use the output of the organize_bus_times function as input.")
  #Completely replace the objects on the given day. 
  BlueBus.objects.filter(day=day).delete()    

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
    store_BlueBus_entry(day, time, name)

    header_index += 1 #NOW save the BlueBus object to the database.
    i += 1 #Increment the total number of entries made.
  print "Database entries for \"{}\" updated successfully!".format(day)
 except Exception as e:
  raise Exception("Could not create data entry {}i: {}".format(i, e))

#FUNCTION WRITTEN BY JESSE PAZDERA, LAST UPDATE: 12/7/13
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
	return timetable + org_times(number_of_columns, times)

    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Swat Van   # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class SwatVan(models.Model):
	day = models.CharField(max_length=9)
	time = models.TimeField()
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return "{}: {} ({})".format(self.day, self.time, self.name)

#FUNCTION WRITTEN BY JESSE PAZDERA, LAST UPDATE: 12/7/13
def organize_trico_van(van_route, times):
	if van_route == 'BMC':
		timetable = [['Leave Bryn Mawr', 'Arrive Swarthmore', 'Leave Swarthmore', 'Arrive Bryn Mawr']]
	elif van_route == 'HC':
		timetable = [['Leave Haverford', 'Arrive Swarthmore', 'Leave Swarthmore', 'Arrive Haverford']]
	elif van_route == 'TRI':
		timetable = [['Bryn Mawr to Haverford', 'Haverford to Swarthmore', 'Swarthmore to Haverford', 'Haverford to Bryn Mawr']]
	else:
		raise Exception('Invalid input: Van route must be \"BMC\", \"HC\", or \"TRI\"')
	return timetable + org_times(4, times)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Events # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Event(models.Model):
	title = models.CharField(max_length=10)
	campus = models.CharField(max_length=15)
	location = models.CharField(max_length=25, blank=True, null=True)
	content = models.TextField(blank=True, null=True)
	date = models.DateField()
	url = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return "{}: {} ({})".format(self.campus, self.title, self.date)

#Written by Casey Falk and Jesse Pazdera (12/12/13)
#Last Modified by "    "
#  Store a new entry in the database with the given fields. 
def store_new_Event(data_dict):
 try:
  new_entry = Event(campus, data=data_dict)
  new_entry.campus = campus
  new_entry.save()
 except Exception as e:
  raise Exception("Data entry could not be stored: {}".format(e))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  News # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class News(models.Model):
	publisher = models.CharField(max_length=20)
	title = models.CharField(max_length=70)
	author= models.CharField(max_length=40)
	content = models.TextField(blank=True, null=True)
	date = models.DateField()
	url = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return "{}: {} ({})".format(self.publisher, self.title, self.date)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # #  Dining   # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Dining(models.Model):
	date = models.DateField()
	meal = models.CharField(max_length=10)
	location = models.CharField(max_length=10)
	food = models.CharField(max_length=40)
	number = models.CharField(max_length=4)

	def __unicode__(self):
		return "{}: {} ({})".format(self.meal, self.food, self.date)



#TODO: Add Users
