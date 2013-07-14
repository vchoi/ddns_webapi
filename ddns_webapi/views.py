# Create your views here.

from django.http import HttpResponse, HttpResponseForbidden
from django.views.defaults import permission_denied
from ddns_webapi.models import ResourceRecord, WebapiKey, NsupdateKey
import ddns_webapi.util
from exceptions import Exception

def checkip(request):
	ip = request.META['REMOTE_ADDR']
	return HttpResponse(ip, content_type="text/plain")

def update(request, key, debug=False):
	try:
		apikey = WebapiKey.objects.get(key=key)
	except WebapiKey.DoesNotExist:
		return HttpResponseForbidden('403 Forbidden',content_type='text/plain')

	rr = ResourceRecord.objects.get(webapi_key=apikey)
	nsupdate_key = NsupdateKey.objects.get(resourcerecord=rr)

	rr.data = request.META['REMOTE_ADDR']

	result = 'OK\n'
	try:
		nsupdate = ddns_webapi.util.NsupdateDriver(rr.zone, rr.rr_class, nsupdate_key, rr.server)
		nsupdate.delete(rr.name, rr.ttl, rr.type)
		nsupdate.add(rr.name, rr.ttl, rr.type, rr.data)
		nsupdate.send()
	except ddns_webapi.util.NsupdateDriverException as e:
		result = 'ERROR\n'
		if debug:
			result += str(e.message) + '\n'

	if debug:
		result += '\n'
		result += 'Resource Record: ' + str(rr) +  '\n'
		result += 'Key Type: ' + nsupdate_key.type + '\n'
		result += 'Key Name: ' + nsupdate_key.name +  '\n'

	content_type = 'text/plain'
	response = HttpResponse(result, content_type=content_type)

	return response
