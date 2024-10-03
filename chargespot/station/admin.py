from django.contrib import admin
from station.models import Station

class StationAdmin(admin.ModelAdmin):
    list_display=['name','user','status']
    prepopulated_fields={"slug":("name",)}
    

admin.site.register(Station,StationAdmin)
