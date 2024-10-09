from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


from station.models import Station,Booking,ActivityLog,StaffOnDuty,Charger,ChargerType,StationGallery,StationFeatures,StationFaqs

@csrf_exempt
def check_charger_availability(request):
    if request.method=="POST":
        id = request.POST.get("station-id")
        plugin=request.POST.get("plugin")
        plugout=request.POST.get("plugout")
        num_vehicles=request.POST.get("num_vehicles")
        num_slots=request.POST.get("num_slots")
        charger_type=request.POST.get("charger-type")
        
        station =Station.objects.get(id=id)
        charger_type=ChargerType.objects.get(station=station,slug=charger_type)
        
        print("id ===== ",id)
        print("plugin ===== ",plugin)
        print("plugout ===== ",plugout)
        print("num_vehicles ===== ",num_vehicles)
        print("num_slots ===== ",num_slots)
        print("charger_type ===== ",charger_type)
        print("station ===== ",station)
        print("charger_type ===== ",charger_type)
        
        url = reverse("station:charger_type_detail",args=[station.slug,charger_type.slug])
        url_with_params = f"{url}?station-id={id}&plugin={plugin}&plugout={plugout}&num_vehicles={num_vehicles}&num_slots={num_slots}&charger_type={charger_type}"
        
        return  HttpResponseRedirect(url_with_params)
        
        
