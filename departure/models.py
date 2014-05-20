from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, GEOSException


# Create your models here.
class Agency(models.Model):
    agency_tag = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    
    def __unicode__(self):
        return 'agency: %s, title: %s, region: %s' % (self.agency_tag, self.title, self.region)

class Stop (models.Model):
    tag = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=200, null=True)
    point = models.PointField()
    stop_id = models.IntegerField(null=True)
    route = models.ForeignKey('Route')
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return 'tag: %s, title: %s, shortTitle: %s' \
            % (self.tag, self.title, self.short_title)
    def get_agency_tag(self):
        return self.route.agency.agency_tag
    
    def get_route_tag(self):
        return self.route.tag
    
    def get_point(self):
        return self.point
    
    def get_title(self):
        return self.title
    
    
class Route(models.Model):
    tag = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=200, null=True)
    #stops = models.ManyToManyField(Stop, related_name='stop_list')
    agency = models.ForeignKey(Agency)
    
    def __unicode__(self):
        return 'tag: %s, title: %s, short_title: %s, agency: %s' \
            % (self.tag, self.title, self.short_title, self.agency)
    
    def get_stops(self):
        stop_set=[]
        for stop in self.stops:
            stop_set.append({
                'tag: {0}'.format(stop.tag),
                'title: {0}'.format(stop.title),
                'shortTitle: {0}'.format(stop.short_title),
                'location: {0}'.format(stop.point),
                'stopID: {0}'.format(stop.stop_id),
            })
        return stop_set


    
    

