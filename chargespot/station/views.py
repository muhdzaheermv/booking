from django.shortcuts import render

def index(request):
    return render(request,"station/station.html")

def home(request):
    return render(request,"station/home.html")
