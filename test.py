from departure.models import Stop
from django.contrib.gis.geos import Point
from geopy import geocoders

lawrence = Point((-95.234657999999996, 38.972679999999997))

stop = Stop.objects.get(tag="ho53_o")

