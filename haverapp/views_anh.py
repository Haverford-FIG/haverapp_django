from django.template import RequestContext
from django.shortcuts import render

def anh(request):
	var = "Yay Content!"
	return render(request, "cool_test_page.html", {"my_variable":var})
