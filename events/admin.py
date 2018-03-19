from django.contrib import admin
from events.models import Events,BookDetails,Coupon
# Register your models here.
class EventsAdmin(admin.ModelAdmin):
    #exclude = ('left_seats')
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        self.readonly_fields = []
        self.exclude.append('left_seats')
        self.exclude.append('is_booked')
        if obj and obj.is_booked:
            self.readonly_fields.append('price')
            self.readonly_fields.append('eventdate')
            self.readonly_fields.append('total_seats')
            self.readonly_fields.append('booked_seats')
            #self.readonly_fields = self.model._meta.get_all_field_names()
            #self.exclude.append('price')
            #self.exclude.append('is_booked')
            #self.exclude.append('eventdate')
            #self.readonly_fields = ['price']
            #self.exclude.append('total_seats')
            #self.exclude.append('booked_seats')
        return super(EventsAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Events,EventsAdmin)

class BookDetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(BookDetails,BookDetailsAdmin)

class CouponAdmin(admin.ModelAdmin):
    pass

admin.site.register(Coupon,CouponAdmin)