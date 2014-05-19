#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree as ET, ParseError
from departure.models import Agency, Stop, Route
import urllib2
from django.contrib.gis.geos import Point, GEOSGeometry


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
        for child in stopList.iterfind('route/stop'):
            try:
                s = Stop(tag = child.get('tag'), title = child.get('title'), short_title = child.get('shortTitle'), point = Point(float(child.get('lat')), float(child.get('lon'))), stop_id = child.get('stopId'), route = route)
                s.save()
            except:
                print 'tag:{0}, title:{1}, shortTitle:{2}'.format(child.get('tag'), child.get('title'), child.get('shortTitle'))
                return

parse_stops()
# Passes in list of stops
# Returns sorted tuple of (routetag, stop, (time predictionsx3)) sorted by time until departure
def get_stops(stops, origin):
    urlBase = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a="
    urlAppendix= ""
    currAgency = ""
    depTimes=[]
    for stop in stops:
        agency_tag = stop.get_agency_tag()
        if stop.get_agency_tag() == currAgency:
            route_tag = stop.get_route_tag()
            if currAgency == "":
                urlAppendix = agency_tag
            urlAppendix = urlAppendix + '&stops={0}|{1}'.format(route_tag, stop.tag)
        # Send XML request to nextbus.
        # Then parse data and store/sort
        else:
            xmlTree = ET(file=urllib2.urlopen(urlBase + urlAppendix))
            # Check to see if there are any predictions at all
            # If attribute(dirTitleBecauseNoPredictions) exists, then there are no predictions.
            
            for node in xmlTree.iterfind('predictions'):
                #Get stop tag
                stop_tag = node.get('stopTag')
                #Create list of departure predictions
                stopTimes=[]
                if node.find('direction') is not None:
                    times=[]
                    for prediction in node.find('direction'): #predictions/direction/prediction
                        times.append(prediction.get('minutes'))
                    
                    stopTimes.append({'tag':stop_tag, 'times':times, 'title': node.find('direction').get('title')})

                    # Insert in sorted order to depTimes
                depTimes = insertTimes(depTimes, stopTimes, origin)
            
            #setup for next loop iteration
            currAgency = "{0}".format(stop.get_agency_tag())
            urlAppendix= "{0}".format(currAgency)
        
    return depTimes

#Test this section!!!
#Current sorting algorithm based off distances
#currList has tuple (stop_tag, times, title, distance)
def insertTimes(currList, appendList, origin):
    for stop in appendList:
        # Get stop distance from origin
        stop_point = Stop.get_point(stop)
        flag = False
        appendItem = stop['distance'].append(stop_point.distance(origin))
        for curr in currList:
            # If current in list is closer than new stop, add new stop before current and break.
            if curr['distance'] > stop_point.distance(origin):
                
                currList.insert(currList.index(curr), appendItem)
                flag = True
                break
        if flag is False:
            currList.append(appendItem)
    
    return currList

        

