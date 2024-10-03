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
    