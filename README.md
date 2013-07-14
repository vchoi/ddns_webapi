ddns_webapi - Dynamic DNS Web API server
===========

This Django app receives commands from clients via a REST-like API
and updates IP addresses on nameservers using dynamic updates.

Sample/simple usage:
 $ curl https://ddns.somewhere/ddns/update/N3ZWfgAfMQ9c9bZ7OLwYEc
 OK

Dependencies
. Python
. Django
. dnspython
. A working nameserver configured to accept updates.

Installation
Pretty straightforward. Create a project, download the app, enable the app
and the django admin app.


