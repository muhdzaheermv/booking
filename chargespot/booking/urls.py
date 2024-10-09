from django.urls import path
from booking import views

app_name="booking"

urlpatterns = [
    path("check_charger_aviliability",views.check_charger_availability,name="check_charger_availability")
]
