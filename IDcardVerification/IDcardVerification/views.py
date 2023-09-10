from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, "index.html")

def aboutUS(request):
    return HttpResponse("hi")

def course(request):
    return HttpResponse("hi hi hi")


def coursedetails(request, courseid):
    return HttpResponse(courseid) 