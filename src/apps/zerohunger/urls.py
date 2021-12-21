from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = 'zerohunger'
urlpatterns = [
    url(r'^(?P<topic>.*)/(?P<countryname>.*)/$', views.home, name='search_topic_country'),
    url(r'^(?P<topic>.*)/$', views.home, name='search_topic'),
    url(r'^$', views.home, name='home'),

]
