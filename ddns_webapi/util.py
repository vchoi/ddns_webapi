import dns
import dns.tsigkeyring
import dns.update
import dns.tsig
import dns.rdataclass
import dns.rdatatype
import dns.query
import dns.exception
import dns.resolver
import exceptions

class NsupdateDriverException(exceptions.Exception):
	def __init__(self, message=''):
		super(NsupdateDriverException, self).__init__()
		self.message='NsupdateDriverException: ' + message

class NsupdateDriver():
	def __init__(self, zone, rr_class, key, server=''):
		try:
			self.key_ring = dns.tsigkeyring.from_text({key.name: key.secret})
		except exceptions.Exception:
			raise NsupdateDriverException("Coudn't load key. Check key type and typos.")
		self.key_name = key.name
		self.key_type = dns.tsig.get_algorithm(key.type)
		self.key_type = key.type
		self.zone = zone
		self.server = server.strip()

		self.update = dns.update.Update(zone, dns.rdataclass.from_text(rr_class),
			self.key_ring, self.key_name, self.key_type)

		if self.server == '':
			answers = dns.resolver.query(zone, 'SOA')
			answer = answers[0]
			self.server = str(answer).split(' ')[0][:-1]

	def delete(self, name, ttl, type):
		self.update.delete(name, dns.rdatatype.from_text(type))

	def add(self, name, ttl, type, data):
		self.update.add(name, ttl, dns.rdatatype.from_text(type), data)

	def send(self, timeout=5):

		try:
			response = dns.query.tcp(self.update, self.server, timeout)
		except dns.tsig.PeerBadKey:
			raise NsupdateDriverException("Peer %s didn't know the key we used. (PeerBadKey)" % self.server)
		except dns.tsig.PeerBadSignature:
			raise NsupdateDriverException("Peer %s didn't like the signature we sent. (PeerBadSignature)" % self.server)
		except dns.tsig.PeerBadTime:
			raise NsupdateDriverException("Peer %s didn't like the time we sent. (PeerBadTime)" % self.server)
		except dns.tsig.PeerBadTruncation:
			raise NsupdateDriverException("Peer %s didn't like the ammount of truncation in the TSIG we sent. (PeerBadTruncation)" % self.server)
		except IOError as e:
			raise NsupdateDriverException(str(e) + ' -- Peer %s' % self.server )
		except dns.exception.Timeout as e:
			raise NsupdateDriverException("Timeout reached (%i seconds). Peer %s."% (timeout,self.server))

