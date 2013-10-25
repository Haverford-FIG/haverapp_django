from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

def dawit(request):
	var="Pigs can fly!!!"
	return render(request, "cool_test_page.html", {"my_variable":var})


