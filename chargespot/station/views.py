from django.shortcuts import render
from station.models import Station,Booking,ActivityLog,StaffOnDuty,Charger,ChargerType,StationGallery,StationFeatures,StationFaqs


def home(request):
    return render(request,"station/home.html")

def index(request):
    stations = Station.objects.filter(status="Live")
    context={
        "stations":stations
    }
    
    return render(request,"station/index.html",context)


def station_detail(request,slug):
    station=Station.objects.get(status="Live",slug=slug)
    context = {
        "station":station,
    }
    return render(request,"station/station_detail.html",context)