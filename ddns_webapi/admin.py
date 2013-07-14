from django.contrib import admin
from ddns_webapi.models import ResourceRecord, NsupdateKey, WebapiKey

admin.site.register(ResourceRecord)
admin.site.register(NsupdateKey)
admin.site.register(WebapiKey)
