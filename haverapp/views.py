from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def home_screen(request):
	return render(request, "index.html", {"example_var": "This is the thing I passed!"})
