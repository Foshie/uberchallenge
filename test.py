from departure.nextbus_xml_parser import *

originPoint = Point(float(37.78669109498105), float(-122.39181600337542))

stops = Stop.objects.all().distance(originPoint).order_by('distance')[:20]
print stops
stops = Stop.objects.filter(point__distance_lte=(originPoint, D(mi=dist))).distance(originPoint).order_by('distance')

big_list = get_stops(stops, originPoint)
print big_list

from departure.views import *
originPoint = Point(float(37.78669109498105), float(-122.39181600337542))
print list_stop(originPoint)


from xml.dom.minidom import Document

def appendList(elem):
    elem.setAttribute('tag', 'you it')

doc = Document()
newElem = doc.createElement('new_elem')
appendList(newElem)
print newElem.toprettyxml()

Stop.objects.get()