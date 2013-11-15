from django.core import validators
from django.core.cache import cache

from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

class BlueBusDay(models.Model):
	day = models.CharField(max_length=9)
	time = models.TimeField()
	name = models.CharField(max_length=30)

	def __unicode__(self):
		return "{}: {} ({})".format(self.day, self.time, self.name)
#x = BlueBusDay()
#x.day, x.name = "Monday", "Test Time"
#x.time = datetime.datetime.now().time()
"""
7:10 AM	7:20 AM	7:40 AM	8:00 AM
8:10 AM	8:20 AM	8:30 AM	8:40 AM
 	 	8:40 AM	8:50 AM
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
http://www.brynmawr.edu/transportation/bico.shtml#friday
"""

