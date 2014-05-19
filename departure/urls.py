from django.conf.urls import patterns, url

from models import Agency, Stop, Route
from views import nearby_stop

urlpatterns = patterns('',
    url(r'^home/', nearby_stop)
)