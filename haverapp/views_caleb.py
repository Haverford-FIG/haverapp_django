from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render


# Import the libraries
import urllib2
import datetime
from xml.etree import ElementTree

# This views file will be funneled into all the other files #

def caleb(request):
	var = "Magical variable of page magnificence. Web development got nothing on me."
	return render(request, "cool_test_page.html", {"my_variable":var})

