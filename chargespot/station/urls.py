from django.urls import path

from station import views

app_name="station"

urlpatterns = [
    path("",views.index,name="index")    
]
