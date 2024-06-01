from django.contrib import admin
from rzd.models import Polygon, Vehicle, Fines, Telematics, TripCard, DrivingStyle

# Register your models here.
admin.site.register(Polygon)
admin.site.register(Vehicle)
admin.site.register(Fines)
admin.site.register(Telematics)
admin.site.register(TripCard)
admin.site.register(DrivingStyle)