from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe

import shortuuid
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField

STATION_STATUS=(
    ("Draft","Draft"),
    ("Disabled","Disabled"),
    ("Rejected","Rejected"),
    ("In Review","In Review"),
    ("Live","Live"),
)

ICON_TYPE=(
    ("Bootstrap Icons","Bootstrap Icons"),
    ("Font","Font"),
    ("Box Icons","Box Icons"),
    ("Remi Icons","Remi Icons"),
    ("Flat Icons","Flat Icons"),
)

PAYMENT_STATUS=(
    ("paid","paid"),
    ("pending","pending"),
    ("processing","processing"),
    ("cancelled","cancelled"),
    ("initiated","initiated"),
    ("failed","failed"),
    ("refunding","refunding"),
    ("refunded","refunded"),
    ("unpaid","unpaid"),
    ("expired","expired"),
)


class Station(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL ,null=True)
    name=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    image=models.FileField(upload_to="station_gallery")
    address=models.CharField(max_length=200)
    mobile=models.CharField(max_length=200)
    email=models.EmailField(max_length=100)
    status=models.CharField(max_length=20,choices=STATION_STATUS,default='Live')
    
    tags = models.CharField(max_length=200,help_text="seperate tags with comma")
    views=models.IntegerField(default=0)
    featured=models.BooleanField(default=False)
    sid=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    slug=models.SlugField(unique=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
       if self.slug == "" or self.slug == None:
           uuid_key=shortuuid.uuid()
           uniqueid=uuid_key[:4]
           self.slug=slugify(self.name) + '-' + str(uniqueid.lower())
       super(Station,self).save(*args,**kwargs)    
           
           
        
            
    def thumbnail(self):
        return mark_safe("<img src='%s' width='50' height='50' style='objects-fit:cover; border-radius:6px;'>" % (self.image.url))
    
class StationGallery(models.Model):
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    image = models.FileField(upload_to="station_gallery")
    sgid=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    
    
    def __str__(self):
        return str(self.station.name)
    

    class Meta:
        verbose_name_plural = "Station Gallery"
        
class StationFeatures(models.Model):
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=100,null=True,blank=True,choices=ICON_TYPE)
    icon=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return str(self.name)
    

    class Meta:
        verbose_name_plural = "Station Features"
        
class StationFaqs(models.Model):
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    question=models.CharField(max_length=1000)
    answer=models.CharField(max_length=1000,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.question)
    

    class Meta:
        verbose_name_plural = "Station FAQs"
        
class ChargerType(models.Model):
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    type=models.CharField(max_length=10)
    price=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    number_of_slots=models.PositiveIntegerField(default=0)
    charger_capacity=models.PositiveIntegerField(default=0)
    ctid=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    slug=models.SlugField(unique=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{str(self.type)} = {self.station.name} - {self.price}"
    

    class Meta:
        verbose_name_plural = "Charger Types"
        
    def chargers_count(self):
        Charger.object.filter(charger_type=self).count()
        
    def save(self,*args,**kwargs):
       if self.slug == "" or self.slug == None:
           uuid_key=shortuuid.uuid()
           uniqueid=uuid_key[:4]
           self.slug=slugify(self.name) + '-' + str(uniqueid.lower())
       super(ChargerType,self).save(*args,**kwargs) 
       
class Charger(models.Model):
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    charger_type = models.ForeignKey(ChargerType,on_delete=models.SET_NULL,null=True,blank=True)
    charger_number=models.CharField(max_length=1000)
    is_available = models.BooleanField(default=True)
    cid=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{str(self.type)} = {self.station.name} - {self.price}"
    

    class Meta:
        verbose_name_plural = "Chargers"
        
    def price(self):
        return self.charger_type.price
    
    def number_of_slots(self):
        return self.charger_type.number_of_slots
    
class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    payment_status=models.CharField(max_length=100,choices=PAYMENT_STATUS)
    
    full_name=models.CharField(max_length=1000)
    email=models.EmailField(max_length=1000)
    phone=models.CharField(max_length=1000)
    
    station = models.ForeignKey(Station,on_delete=models.SET_NULL,null=True,blank=True)
    charger_type = models.ForeignKey(ChargerType,on_delete=models.SET_NULL,null=True,blank=True)
    charger=models.ManyToManyField(Charger)
    before_discount=models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    total=models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    saved=models.DecimalField(max_digits=12, decimal_places=2,default=0.00)
    
    charging_start_time = models.DateField()
    charging_end_time = models.DateField()
    
    total_days=models.PositiveIntegerField(default=0)
    num_vehicles=models.PositiveIntegerField(default=1)
    num_slots=models.PositiveIntegerField(default=0)
    
    plugged_in = models.BooleanField(default=False)
    unplugged = models.BooleanField(default=False)
    
    is_active=models.BooleanField(default=False)
    
    plugged_in_tracker = models.BooleanField(default=False)
    unplugged_tracker = models.BooleanField(default=False)
    
    bid=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    date=models.DateTimeField(auto_now_add=True)
    stripe_payment_intent=models.CharField(max_length=1000,null=True,blank=True)
    success_id=models.CharField(max_length=1000,null=True,blank=True)
    booking_id=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    
    def __str__(self):
        return f"{self.booking_id}"
    
    def chargers(self):
        return self.room.all().count()
    
class ActivityLog(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    guess_out=models.DateTimeField()
    guess_in=models.DateTimeField()
    description=models.TextField(null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.booking}"
    
class StaffOnDuty(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    staff_id=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.staff_id}"
    
    
    
    

    
    

    
        
        
    

    
    
    
    
    
    
    
    
        
