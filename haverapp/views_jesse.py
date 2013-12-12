from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#ALL FUNCTIONS WRITTEN BY JESSE PAZDERA, LAST UPDATE: 12/7/13

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
'''
MONDAY:

7:25 AM	7:35 AM	7:40 AM	7:50 AM
8:10 AM	8:20 AM	8:40 AM	8:50 AM
\t \t 8:50 AM	9:00 AM
9:10 AM	9:20 AM	9:40 AM	9:50 AM
9:20 AM	9:30 AM	9:50 AM	10:00 AM
10:00 AM	10:10 AM	10:15 AM	10:25 AM
10:10 AM	10:20 AM	10:25 AM	10:35 AM
10:30 AM	10:40 AM	10:40 AM	10:50 AM
10:40 AM	10:50 AM	10:50 AM	11:00 AM
11:00 AM	11:10 AM	11:15 AM	11:25 AM
11:10 AM	11:20 AM	11:25 AM	11:35 AM
11:30 AM	11:40 AM	11:45 AM	11:55 AM
11:40 AM	11:50 AM	11:55 AM	12:05 PM
12:00 PM	12:10 PM	12:15 PM	12:25 PM
12:10 PM	12:20 PM	12:25 PM	12:35 PM
12:30 PM	12:40 PM	12:45 PM	12:55 PM
12:40 PM	12:50 PM	12:55 PM	1:05 PM
1:00 PM	1:10 PM	1:15 PM	1:25 PM
1:10 PM	1:20 PM	1:25 PM	1:35 PM
1:30 PM	1:40 PM	1:45 PM	1:55 PM
1:40 PM	1:50 PM	1:55 PM	2:05 PM
2:00 PM	2:10 PM	2:15 PM	2:25 PM
2:10 PM	2:20 PM	2:25 PM	2:35 PM
2:35 PM	2:45 PM	2:50 PM	3:00 PM
3:10 PM	3:20 PM	3:30 PM	3:40 PM
3:20 PM	3:30 PM	3:40 PM	3:30 PM
3:45 PM	3:55 PM	4:00 PM	4:10 PM
3:55 PM	4:05 PM	4:10 PM	4:20 PM
4:15 PM	4:25 PM	4:45 PM	4:55 PM
5:10 PM	5:20 PM	5:50 PM	6:00 PM
6:10 PM 	6:20 PM	6:25 PM	6:35 PM
6:40 PM	6:50 PM	6:55 PM	7:05 PM
7:10 PM	7:20 PM	7:40 PM	7:50 PM
8:10 PM	8:20 PM	8:55 PM	9:05 PM
9:10 PM	9:20 PM	10:05 PM	10:15 PM
10:20 PM	10:30 PM	10:40 PM	10:50 PM
11:10 PM	11:20 PM	11:40 PM	11:50 PM
12:10 AM	12:20 AM	12:40 AM	12:50 AM

TUESDAY:

7:10 AM	7:20 AM	7:40 AM	8:00 AM
8:10 AM	8:20 AM	8:30 AM	8:40 AM
\t \t 8:40 AM	8:50 AM
8:55 AM	9:05 AM	9:20 AM	9:30 AM
9:05 AM	9:15 AM	9:30 AM	9:40 AM
9:45 AM	9:55 AM	10:00 AM	10:10 AM
9:55 AM	10:05 AM	10:10 AM	10:20 AM
10:25 AM	10:35 AM	10:45 AM	10:55 AM
10:35 AM	10:45 AM	10:55 AM	11:05 AM
11:10 AM	11:20 AM	11:30 AM	11:40 AM
11:20 AM	11:30 AM	11:40 AM	11:50 AM
11:55 AM	12:05 PM	12:15 PM	12:25 PM
12:05 PM	12:15 PM	12:25 PM	12:35 PM
12:45 PM	12:55 PM	1:00 PM	1:10 PM
12:50 PM	1:00 PM	1:10 PM	1:20 PM
1:25 PM	1:35 PM	1:45 PM	1:55 PM
1:35 PM	1:45 PM	1:55 PM	2:05 PM
2:10 PM	2:20 PM	2:40 PM	2:50 PM
2:25 PM	2:35 PM	2:50 PM	3:00 PM
3:10 PM	3:20 PM	3:30 PM	3:40 PM
3:20 PM	3:30 PM	3:40 PM	3:50 PM
3:45 PM	3:55 PM	4:00 PM	4:10 PM
3:55 PM	4:05 PM	4:10 PM	4:20 PM
4:15 PM	4:25 PM	4:45 PM	4:55 PM
5:10 PM	5:20 PM	5:50 PM	6:00 PM
6:10 PM	6:20 PM	6:25 PM	6:35 PM
6:40 PM	6:50 PM	6:55 PM	7:05 PM
7:10 PM	7:20 PM	7:40 PM	7:50 PM
8:10 PM	8:20 PM	8:55 PM	9:05 PM
9:10 PM	9:20 PM	10:05 PM	10:15 PM
10:20 PM	10:30 PM	10:40 PM	10:50 PM
11:10 PM	11:20 PM	11:40 PM	11:50 PM
12:10 AM	12:20 AM	12:40 AM	12:50 AM

WEDNESDAY:

7:25 AM	7:35 AM	7:40 AM	7:50 AM
8:10 AM	8:20 AM	8:40 AM	8:50 AM
\t \t 8:50 AM	9:00 AM
9:10 AM	9:20 AM	9:40 AM	9:50 AM
9:20 AM	9:30 AM	9:50 AM	10:00 AM
10:00 AM	10:10 AM	10:15 AM	10:25 AM
10:10 AM	10:20 AM	10:25 AM	10:35 AM
10:30 AM	10:40 AM	10:40 AM	10:50 AM
10:40 AM	10:50 AM	10:50 AM	11:00 AM
11:00 AM	11:10 AM	11:15 AM	11:25 AM
11:10 AM	11:20 AM	11:25 AM	11:35 AM
11:30 AM	11:40 AM	11:45 AM	11:55 AM
11:40 AM	11:50 AM	11:55 AM	12:05 PM
12:00 PM	12:10 PM	12:15 PM	12:25 PM
12:10 PM	12:20 PM	12:25 PM	12:35 PM
12:30 PM	12:40 PM	12:45 PM	12:55 PM
12:40 PM	12:50 PM	12:55 PM	1:05 PM
1:00 PM	1:10 PM	1:15 PM	1:25 PM
1:10 PM	1:20 PM	1:25 PM	1:35 PM
1:30 PM	1:40 PM	1:45 PM	1:55 PM
1:40 PM	1:50 PM	1:55 PM	2:05 PM
2:00 PM	2:10 PM	2:15 PM	2:25 PM
2:10 PM	2:20 PM	2:25 PM	2:35 PM
2:35 PM	2:45 PM	2:50 PM	3:00 PM
3:10 PM	3:20 PM	3:30 PM	3:40 PM
3:20 PM	3:30 PM	3:40 PM	3:50 PM
3:45 PM	3:55 PM	4:00 PM	4:10 PM
3:55 PM	4:05 PM	4:10 PM	4:20 PM
4:15 PM	4:25 PM	4:45 PM	4:55 PM
5:10 PM	5:20 PM	5:50 PM	6:00 PM
6:00 PM	6:10 PM	6:15 PM	6:25 PM
6:30 PM	6:40 PM	6:55 PM	7:05 PM
7:10 PM	7:20 PM	7:40 PM	7:50 PM
8:10 PM	8:20 PM	8:55 PM	9:05 PM
9:10 PM	9:20 PM	10:05 PM	10:15 PM
10:20 PM	10:30 PM	10:40 PM	10:50 PM
11:10 PM	11:20 PM	11:40 PM	11:50 PM
12:10 AM	12:20 AM	12:40 AM	12:50 AM

THURSDAY:

7:10 AM	7:20 AM	7:40 AM	8:00 AM
8:10 AM	8:20 AM	8:30 AM	8:40 AM
\t \t 8:40 AM	8:50 AM
8:55 AM	9:05 AM	9:20 AM	9:30 AM
9:05 AM	9:15 AM	9:30 AM	9:40 AM
9:45 AM	9:55 AM	10:00 AM	10:10 AM
9:55 AM	10:05 AM	10:10 AM	10:20 AM
10:25 AM	10:35 AM	10:45 AM	10:55 AM
10:35 AM	10:45 AM	10:55 AM	11:05 AM
11:10 AM	11:20 AM	11:30 AM	11:40 AM
11:20 AM	11:30 AM	11:40 AM	11:50 AM
11:55 AM	12:05 PM	12:15 PM	12:25 PM
12:05 PM	12:15 PM	12:25 PM	12:35 PM
12:40 PM	12:50 PM	1:00 PM	1:10 PM
12:50 PM	1:00 PM	1:10 PM	1:20 PM
1:25 PM	1:35 PM	1:45 PM	1:55 PM
1:35 PM	1:45 PM	1:55 PM	2:05 PM
2:10 PM	2:20 PM	2:40 PM	2:50 PM
2:25 PM	2:35 PM	2:50 PM	3:00 PM
3:10 PM	3:20 PM	3:30 PM	3:40 PM
3:20 PM	3:30 PM	3:40 PM	3:50 PM
3:45 PM	3:55 PM	4:00 PM	4:10 PM
3:55 PM	4:05 PM	4:10 PM	4:20 PM
4:15 PM	4:25 PM	4:45 PM	4:55 PM
5:10 PM	5:20 PM	5:50 PM	6:00 PM
6:10 PM	6:20 PM	6:25 PM	6:35 PM
6:40 PM	6:50 PM	6:55 PM	7:05 PM
7:10 PM	7:20 PM	7:40 PM	7:50 PM
8:10 PM	8:20 PM	8:55 PM	9:05 PM
9:10 PM	9:20 PM	9:35 PM	9:45 PM
9:50 PM	10:00 PM	10:05 PM	10:15 PM
10:20 PM	10:30 PM	10:40 PM	10:50 PM
11:10 PM	11:20 PM	11:40 PM	11:50 PM
12:10 AM	12:20 AM	12:40 AM	12:50 AM

FRIDAY:

7:25 AM	7:35 AM	7:40 AM	7:50 AM
8:10 AM	8:20 AM	8:40 AM	8:50 AM
\t \t 8:50 AM	9:00 AM
9:10 AM	9:20 AM	9:40 AM	9:50 AM
9:20 AM	9:30 AM	9:50 AM	10:00 AM
10:00 AM	10:10 AM	10:15 AM	10:25 AM
10:10 AM	10:20 AM	10:25 AM	10:35 AM
10:30 AM	10:40 AM	10:40 AM	10:50 AM
10:40 AM	10:50 AM	10:50 AM	11:00 AM
11:00 AM	11:10 AM	11:15 AM	11:25 AM
11:10 AM	11:20 AM	11:25 AM	11:35 AM
11:30 AM	11:40 AM	11:45 AM	11:55 AM
11:40 AM	11:50 AM	11:55 AM	12:05 PM
12:00 PM	12:10 PM	12:15 PM	12:25 PM
12:30 PM	12:40 PM	12:45 PM	12:55 PM
1:00 PM	1:10 PM	1:15 PM	1:25 PM
1:30 PM	1:40 PM	1:45 PM	1:55 PM
2:00 PM	2:10 PM	2:15 PM	2:25 PM
2:35 PM	2:45 PM	2:50 PM	3:00 PM
3:10 PM	3:20 PM	3:30 PM	3:40 PM
3:45 PM	3:55 PM	4:00 PM	4:10 PM
4:15 PM	4:25 PM	4:45 PM	4:55 PM
5:10 PM	5:20 PM	5:50 PM	6:00 PM
6:10 PM 	6:20 PM	6:25 PM	6:35 PM
6:40 PM	6:50 PM	6:55 PM	7:05 PM
7:10 PM	7:20 PM	7:40 PM	7:50 PM
8:10 PM	8:20 PM	8:55 PM	9:05 PM
9:10 PM	9:20 PM	10:05 PM	10:15 PM
10:20 PM	10:30 PM	10:40 PM	10:50 PM
11:10 PM	11:20 PM	11:40 PM	11:50 PM
12:10 AM	12:20 AM	12:40 AM	12:50 AM
1:10 AM	1:20 AM	1:40 AM	1:50 AM
2:00 AM	2:10 AM	2:40 AM	2:50 AM

SATURDAY (Day):

11:15 AM	11:25 AM	11:35 AM	11:40 AM	11:50 AM
12:15 PM	12:25 PM	12:35 PM	12:40 PM	12:50 PM
1:15 PM	1:25 PM	1:35 PM	1:40 PM	1:50 PM
2:15 PM	2:25 PM	2:35 PM	2:40 PM	2:50 PM

SATURDAY (Night):

5:00 PM	5:15 PM
5:30 PM	5:45 PM
6:00 PM	6:15 PM
6:30 PM	6:45 PM
7:00 PM	7:15 PM
7:30 PM	7:45 PM
8:00 PM	8:15 PM
9:00 PM	9:15 PM
10:00 PM	10:15 PM
10:30 PM	10:45 PM
11:00 PM	11:15 PM
12:00 AM	12:15 AM
12:30 AM	12:45 AM
1:00 AM	1:30 AM
2:00 AM	2:30 AM
2:45 AM	3:00 AM

SUNDAY:

9:30 AM	9:45 AM
10:15 AM	10:45 AM
11:30 AM	11:45 AM
12:30 PM	12:45 PM
1:30 PM	1:45 PM
2:30 PM	2:45 PM
3:30 PM	3:45 PM
5:00 PM	5:15 PM
5:30 PM	5:45 PM
6:00 PM	6:15 PM
6:30 PM	6:45 PM
7:00 PM	7:15 PM
8:00 PM	8:15 PM
9:00 PM	9:15 PM
10:00 PM	10:15 PM
11:00 PM	11:15 PM
12:00 AM	12:15 AM
'''
