from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

def index(request):
    return HttpResponse("The main page")

def about(request, webid):
    if webid:
        print(webid)
    else:
        return redirect('home', permanent=True)
    return HttpResponse(f"About page<p>{webid}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound("Page not found...")