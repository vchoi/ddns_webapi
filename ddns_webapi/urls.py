from django.conf.urls.defaults import patterns, include, url
#from django.conf.urls import patterns, url

urlpatterns = patterns('ddns_webapi.views',
	url(r'^checkip$', 'checkip'),
	url(r'^update/(?P<key>[0-9a-zA-Z]+)$', 'update'),
	url(r'^update/(?P<key>[0-9a-zA-Z]+)/debug$', 'update', {'debug': True}),
)
