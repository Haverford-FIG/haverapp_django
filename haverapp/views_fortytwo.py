from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def fortytwo(request):
	dove = "the square root of two = " + str(2**.5)
	return render(request, "index.html", {"sparrow":dove})


