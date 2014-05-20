from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.template import RequestContext
from django.shortcuts import render_to_response
import datetime

from models import Agency, Stop, Route
import nextbus_xml_parser
# Generates a view for nearest stops within .5 miles of the users current location.
def nearby_stop(request):
    origin = Point (33.884736,-118.41090899999999)
    if request.GET.get('lat') and request.GET.get('lon'):
        origin = Point(float(request.GET.get('lat')), float(request.GET.get('lon')))
        stops = list_stop(origin)
    else:
        stops = Stop.objects.all().order_by('tag')[:20]
    return render_to_response('gmap3.html', {
        'stop_list': stops,
        'lon': '{0}'.format(origin.get_y()),
        'lat': '{0}'.format(origin.get_x()),
    }, context_instance=RequestContext(request))

def list_stop(origin):
    
    stops = Stop.objects.all().distance(origin).order_by('distance')[:20]
    
    sorted_stops = nextbus_xml_parser.get_stops(stops, origin)
    
    return stops


    