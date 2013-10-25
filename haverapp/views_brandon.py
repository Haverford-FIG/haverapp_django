from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def brandon(request):
	var =  "Hello everybody"
	return render(request, "cool_test_page.html", {"my_variable":var})

def get_events(request):
	return HtmlResponse("<h1>Come Check out the Events!</h1>")


