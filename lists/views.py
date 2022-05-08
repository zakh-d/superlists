from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return HttpResponse('<html><title>To-Do list</title></html>')

