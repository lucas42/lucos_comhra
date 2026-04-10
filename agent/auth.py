import re, requests, urllib.parse
from flask import request, redirect

valid_tokens = [] # A cache of tokens which are known to be valid

class AuthException(Exception):
	pass

def checkAuth():
	token = request.args.get('token') or request.cookies.get('token')
	if not token:
		raise AuthException("No token found")
	if token in valid_tokens:
		return True
	try:
		response = requests.get('https://auth.l42.eu/data?'+urllib.parse.urlencode({'token': token}))
		response.raise_for_status() # Invalid tokens will return a 401 response
		valid_tokens.append(token)
		return True
	except Exception as error:
		print ("\033[91m** Authentication Error ** " + str(error) + "\033[0m", flush=True)
		raise AuthException(str(error))

def authenticate():
	redirect_url = "{}://{}{}".format(request.headers.get('X-Forwarded-Proto', 'http'), request.headers.get('Host'), request.path)
	return redirect("https://auth.l42.eu/authenticate?"+urllib.parse.urlencode({'redirect_uri': redirect_url}))

SAFE_TOKEN_RE = re.compile(r'^[a-zA-Z0-9\-_]+\Z')

def setAuthCookies(response):
	token = request.args.get('token')
	if token is not None and SAFE_TOKEN_RE.match(token) and request.cookies.get('token') != token:
		if token in valid_tokens:
			response.set_cookie('token', token)
	return response