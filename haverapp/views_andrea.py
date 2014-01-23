from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render

#Import the libraries to parse xml and strip it.
import urllib2
import datetime
from xml.etree import ElementTree

