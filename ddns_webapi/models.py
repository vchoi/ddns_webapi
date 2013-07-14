from django.db import models

# Create your models here.

KEY_DIGITS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY_LENGTH = 22
KEY_BASE = len(KEY_DIGITS)

def _gen_key():
	from random import SystemRandom
	r = SystemRandom()
	l = r.randrange(len(KEY_DIGITS)**KEY_LENGTH)
	key = ''
	while l >= KEY_BASE:
		remainder = l % KEY_BASE
		key += KEY_DIGITS[remainder]
		l = l / KEY_BASE
	key += KEY_DIGITS[l]
	key = key[::-1]
	return key

class WebapiKey(models.Model):
	key = models.CharField(max_length=KEY_LENGTH, default=_gen_key, unique=True)
	access_time = models.DateTimeField('access time')
	access_count = models.IntegerField(default=0)
	credits = models.IntegerField(default=100)
	cost = models.IntegerField(default=100)
	income = models.IntegerField(default=100)

	def __unicode__(self):
		return self.key

class NsupdateKey(models.Model):
	KEY_TYPES = (
		('hmac-sha512', 'hmac-sha512'),
		('hmac-sha384', 'hmac-sha384'),
		('hmac-sha256', 'hmac-sha256'),
		('hmac-sha224', 'hmac-sha224'),
		('hmac-sha1', 'hmac-sha1'),
		('HMAC-MD5.SIG-ALG.REG.INT', 'hmac-md5'),
	)

	name = models.CharField(max_length=512, blank=False)
	type = models.CharField(max_length=30, blank=False, default='hmac-sha512', choices=KEY_TYPES)
	secret = models.CharField(max_length=100, blank=False)

	def __unicode__(self):
		return self.name

class ResourceRecord(models.Model):
	RR_CLASS = (
		('IN', 'Internet'),
		('CH', 'Chaos'),
		('HS', 'Hesiod'),
	)
	RR_TYPES = (
		('A', 'A'),
		('AAAA', 'AAAA'),
	)

	name = models.CharField(max_length=63, blank=False)
	zone = models.CharField(max_length=253, blank=False)
	ttl = models.IntegerField(default=60)
	rr_class = models.CharField(max_length=2, choices=RR_CLASS, default='IN')
	type = models.CharField(max_length=4, choices=RR_TYPES, default='A')
	data = models.CharField(max_length=65535, blank=True)
	
	webapi_key = models.OneToOneField(WebapiKey)
	nsupdate_key = models.ForeignKey(NsupdateKey)
	server = models.CharField(max_length=253, blank=True, help_text="Leave empty for automatic discovery.")

	def _bind_notation(self):
		return "%s.%s %i %s %s %s" % (self.name, self.zone, self.ttl, self.rr_class, self.type, self.data)

	def __unicode__(self):
		return self._bind_notation()
