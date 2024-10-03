from django.urls import path

from station import views

app_name="station"

urlpatterns = [
    path("",views.home,name="home") ,   
    path("index",views.index,name="index")    
]
