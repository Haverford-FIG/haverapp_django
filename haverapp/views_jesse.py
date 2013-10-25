from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def jesse(request):
	var = "I'm Commander Shepard, and this is my favorite store on the Citadel!"
	return render(request, "cool_test_page.html", {"my_variable":var})
