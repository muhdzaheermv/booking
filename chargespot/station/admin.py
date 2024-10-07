from django.contrib import admin
from station.models import Station,Booking,ActivityLog,StaffOnDuty,Charger,ChargerType,StationGallery,StationFeatures,StationFaqs

class StationGalleryInline(admin.TabularInline):
    model=StationGallery

class StationAdmin(admin.ModelAdmin):
    inlines=[StationGalleryInline]
    list_display=['thumbnail','user','name','status']
    prepopulated_fields={"slug":("name",)}
    

admin.site.register(Station,StationAdmin)
admin.site.register(Booking)
admin.site.register(ActivityLog)
admin.site.register(StaffOnDuty)
admin.site.register(Charger)
admin.site.register(ChargerType)
admin.site.register(StationGallery)
admin.site.register(StationFeatures)
admin.site.register(StationFaqs)
