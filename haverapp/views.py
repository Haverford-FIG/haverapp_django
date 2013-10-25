from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render


def home_screen(request):
	return render(request, "index.html")

def health(request):
	return render(request, "health.html")

def events(request):
	return HttpResponse("Yay! We have an events page!")
