from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("The main page")

def about(request):
    return HttpResponse("About page")