from django.db import models

# Create your models here.
class Events(models.Model):
    #user = models.ForeignKey(User,on_delete=None)
    events_type = models.CharField(max_length=250)
    #created_by = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    #art_hidden = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,blank=True)
    is_booked = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    total_seats = models.IntegerField(default=0)
    left_seats = models.IntegerField(default=0)
    booked_seats = models.CharField(max_length=2000,blank=True)
    cover_logo = models.FileField()
    eventdate = models.DateField(default=None)

    def __str__(self):
        return self.events_type + ' - ' + self.description

class BookDetails(models.Model):
    event = models.ForeignKey(Events,on_delete=None)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    booked_seats = models.CharField(max_length=250)
    count = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    txnid = models.CharField(max_length=75,default='')
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)

class Coupon(models.Model):
    event = models.ForeignKey(Events,on_delete=None)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)
    coupon_code = models.CharField(max_length=5)
    discount_percent = models.IntegerField(default=0)
    is_activated = models.BooleanField(default=False)
