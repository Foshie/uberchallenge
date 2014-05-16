from django.db import models



# Create your models here.
class Agency(models.Model):
    agency_tag = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    region = models.CharField(max_length=30)
    
    def __str___(self):
        return 'agency: %s, title: %s, region: %s' % (self.agency_tag, self.title, self.region)
    
    
class Stop (models.Model):
    tag = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=30)
    lat = models.FloatField()
    lon = models.FloatField()
    stopID = models.IntegerField()
    
    def __str__(self):
        return 'tag: %s, title: %s, shortTitle: %s, lat: %f, lon: %f, stopID: %d' \
            % (self.tag, self.title, self.short_title, self.lat, self.lon, self.stopID)
    
class Route(models.Model):
    tag = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=30)
    stops = models.ManyToManyField(Stop)
    agency = models.ForeignKey(Agency)
    
    def __str__(self):
        return 'tag: %s, title: %s, short_title: %s, agency: %s' \
            % (self.tag, self.title, self.short_title, self.agency)
    

    
    

