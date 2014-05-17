from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Agency, Stop, Route

# Create your views here.
def nearby_stop(request):
    if request.GET.get('lat') and request.GET.get('lon'):
        origin = Point(float(request.GET.get('lat')), float(request.Get.get('lon')))
        stops = Stop.objects.all()