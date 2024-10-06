from django.contrib import admin
from station.models import Station,Booking,ActivityLog,StaffOnDuty,Charger,ChargerType

class StationAdmin(admin.ModelAdmin):
    list_display=['thumbnail','user','name','status']
    prepopulated_fields={"slug":("name",)}
    

admin.site.register(Station,StationAdmin)
admin.site.register(Booking)
