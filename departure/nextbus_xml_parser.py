#!/usr/bin/env python
import sys
from xml.etree.ElementTree import ElementTree as ET, ParseError
from departure.models import Agency, Stop, Route
import urllib2
from django.contrib.gis.geos import Point, GEOSGeometry
from urllib2 import HTTPError

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
            for child in stopList.iterfind('route/stop'):
                print child.attrib
                s = Stop(tag = child.get('tag'), title = child.get('title'), short_title = child.get('shortTitle'), point = Point(float(child.get('lat')), float(child.get('lon'))), stop_id = child.get('stopId') ,route = route)
                s.save()
        
        except urllib2.URLError as e:
            print "unable to connect to url for agency"# {0}, {1}".format(route.agency.agency_tag, route.tag)
            print e
        except:
            print 'tag:{0}, title:{1}, shortTitle:{2}'.format(child.get('tag'), child.get('title'), child.get('shortTitle'))
            return

#parse_stops()
def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))
# Passes in list of stops
# Returns sorted tuple of (routetag, stop, (time predictionsx3)) sorted by time until departure
def get_stops(stops, origin):
    urlArray=[]
    #1 method - Guaranteed 2 pass through storage:
    # Can Probably refine the search method.
    keys = []
    # First iteration generates keys for agency
    for stop in stops:
        agency_tag = stop.get_agency_tag().__str__()
        if agency_tag not in keys:
            keys.append(agency_tag)
    print 'Keys: {0}'.format(keys)
    # Second iteration creates dictionary of stops.
    urlDict = { a_tag: [] for a_tag in keys}
    print urlDict
    for stop in stops:
        agency_tag = stop.get_agency_tag()
        route_tag = stop.get_route_tag().__str__()
        stopURL = "{0}|{1}".format(route_tag, stop.tag)
        urlDict[agency_tag].append(stopURL)
    
    print 'Dictionary: {0}'.format(urlDict)
    # Generate url appendix for each entry in the dictionary        
    for key in urlDict:
        urlArray.append(generate_multiStopURL(key,urlDict[key]))
    print urlArray
    return parse_multiStop(urlArray, origin)
def generate_multiStopURL(key, value):
    urlBase = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a="
    urlAppendix = key
    for stop in value:
        urlAppendix = urlAppendix + '&stops={0}'.format(stop)
    
    return urlBase + urlAppendix
    
# Returns a list of dictionaries: {'tag':'tag', 'times':[times], 'direction', 'direction'}
def parse_multiStop(urlArray, origin):
    depTimes=[]
    for urlPath in urlArray:
        try:
            xmlTree = ET(file=urllib2.urlopen(urlPath))
            print urlPath
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
                    
                    stopTimes.append({'tag':stop_tag, 'times':times,'direction': node.find('direction').get('title').__str__()})
                
                    # Insert in sorted order to depTimes
                    depTimes = insertTimes(depTimes, stopTimes, origin)
                    
        except HTTPError as e:
            print e
            print urlPath
            sys.exit(0)       
    return depTimes         
#Test this section!!!
#Current sorting algorithm based off distances
#currList is a list of dictionary:(stop:[stop_tag, times, direction], title:title, distance:distance)
def insertTimes(currList, appendList, origin):
    print 'List: {0}'.format(currList)
    for stop in appendList:
        # Get stop distance from origin
        sList = list(Stop.objects.filter(tag=stop['tag']))
        stop_point = sList[0].get_point()
        flag = False
        #Add title to the stop dictionary
        stop_title = sList[0].get_title().__str__()
        appendItem = {'stop':[stop], 'title':stop_title, 'distance':stop_point.distance(origin)}
        print 'Append: {0}'.format(appendItem)
        #Where does it go
        for curr in currList:
            print 'Stop: {0}'.format(stop)
            if curr['distance'] == stop_point.distance(origin):
                #If distance is the same, && Location is the same ( Same stop title)
                #    Then add stop the list of curr['stop']
                if curr['title'] == stop_title:
                    curr['stop'].append(stop)
                #Otherwise insert into list as new entry before current.
                else:
                    currList.insert(currList.index(curr), appendItem)
                flag = True
                break
            # If current in list is closer than new stop, add new stop before current and break.
            elif curr['distance'] > stop_point.distance(origin):                
                currList.insert(currList.index(curr), appendItem)
                flag = True
                break
        if flag is False:
            currList.append(appendItem)
    
    return currList

        

