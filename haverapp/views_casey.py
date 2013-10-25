from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def casey(request):
	var = "This is my page! yaaay --socool #yoloswag"
	return render(request, "cool_test_page.html", {"my_variable":var})
