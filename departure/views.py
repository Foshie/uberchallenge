from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.template import RequestContext
from django.shortcuts import render_to_response

from models import Stop

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
    
    #Generate a generic stop list within 1 mile of the user.
    #This is all by preference: If get_stops does not come back with more than 20 individual stops, 
    #then expand the search  
    dist=0.2
    #while len(sorted_stops) < 20:
    stops = Stop.objects.filter(point__distance_lte=(origin, D(mi=dist))).distance(origin).order_by('distance')
    sorted_stops = nextbus_xml_parser.get_stops(stops, origin)
    #dist = dist + 1 # Expand search by 1 mile each time
    return sorted_stops


    