import re, os, json
import urlparse
import urllib, urllib2
from contextlib import closing
import json
import random
import string

SECRET_LENGTH = 32

# Find all urls in a string
def extract_urls(s):
	return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)

# is this url a youtube url?
def is_youtube(url):
	youtube_regex = (
		r'(https?://)?(www\.)?'
		'(youtube|youtu|youtube-nocookie)\.(com|be)/')
	return re.match(youtube_regex, url)

# A helper function to pretty-print Python objects as JSON
def pp(o): 
    print json.dumps(o, indent=1)

# 
def encode_uri(uri, params):
  encoded_params = urllib.urlencode(params)
  return uri + '?' + encoded_params

def get_request(uri, params, format='json'):
  encoded_uri = encode_uri(uri, params)
  with closing(urllib2.urlopen(encoded_uri)) as request:
    raw_response = request.read().decode('utf-8')
    if format == 'query':
      response = urlparse.parse_qs(raw_response)
    elif format == 'json':
      response = json.loads(raw_response)
    else:
      raise ValueError('invalid format: %s')
  return response

def gen_secret():
  return ''.join(random.choice(string.hexdigits) for n in range(SECRET_LENGTH))