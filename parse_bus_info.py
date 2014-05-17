#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree as ET, ParseError
from departure.models import Agency, Stop, Route
import urllib2.URLError
import urllib2
from django.contrib.gis.geos import Point, GEOSException


def parse_agency():
    try:
        agencyList = ET(file = "/home/josh/projects/xml_files/agencyList.xml")
    except ParseError:
        print "Unable to parse XML from file" 
    
    for agency in agencyList.getiterator('agency'):
        a = Agency(agency_tag = agency.get('tag'), title = agency.get('title'), region = agency.get('regionTitle'))
        a.save()


def parse_routes():
    for agency in Agency.objects.all():
        try:
            if agency.region == 'California-Northern':
                routeList=ET(file=urllib2.urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a={0}".format(agency.agency_tag)))
                for route in routeList.getiterator('route'):
                    r = Route(tag = route.get('tag'), title = route.get('title'), short_title = route.get('shortTitle'),  agency=agency)
                    r.save()
        except urllib2.URLError:
            print "unable to connect to url for agency {0}".format(agency.agency_tag)
        


def parse_stops():
    for route in Route.objects.all():
        try:
            stopList = ET(file=urllib2.urlopen("http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a={0}&r={1}".format(route.agency.agency_tag, route.tag)))
        except urllib2.URLError:
            print "unable to connect to url for agency {0}, {1}".format(route.agency.agency_tag, route.tag)
        root = stopList.getroot()
        for child in root:
            stops = child
            for child in stops:
                if child.tag == 'stop':
                    s = Stop(tag = child.get('tag'), title = child.get('title'), short_title = child.get('shortTitle'), point = Point(float(child.get('lat')), float(child.get('lon'))), stop_id = child.get('stopId'), route = route)
                    s.save()

#parse_agency()
#parse_routes()
#parse_stops()

