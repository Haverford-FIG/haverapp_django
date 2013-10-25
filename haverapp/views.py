from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def home_screen(request):
	lst = ["cats", "dogs", "sheep", "andrea"]
	return render(request, "index.html", {"lst":lst})

def events_page(request):
	return HttpResponse("Yay! We have an events page!")
