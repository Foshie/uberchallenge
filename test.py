from departure.nextbus_xml_parser import *

originPoint = Point(float(37.78669109498105), float(-122.39181600337542))

stops = Stop.objects.all().distance(originPoint).order_by('distance')[:20]
print stops

big_list = get_stops(stops, originPoint)
print big_list
